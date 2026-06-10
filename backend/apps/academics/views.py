from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.access import (
    get_parent_profile,
    get_teacher_profile,
    is_director,
    is_parent,
    is_teacher,
)

from .models import (
    ClassRoom,
    ParentStudentRelation,
    Student,
    Subject,
    TeacherClassAssignment,
    TimetableSession,
)
from .serializers import (
    ClassRoomSerializer,
    ParentStudentRelationSerializer,
    StudentSerializer,
    SubjectSerializer,
    TeacherClassAssignmentSerializer,
    TimetableSessionSerializer,
)


def _boolean_query_value(value):
    return value.lower() in ('1', 'true', 'yes')


class DirectorWriteMixin:
    permission_classes = (IsAuthenticated,)

    def _require_director_with_school(self):
        if not is_director(self.request.user):
            raise PermissionDenied('Only directors can change setup data.')
        if not self.request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

    def _user_school(self):
        return self.request.user.school

    def perform_create(self, serializer):
        self._require_director_with_school()
        serializer.save(school=self._user_school())

    def perform_update(self, serializer):
        self._require_director_with_school()
        serializer.save(school=self._user_school())

    def destroy(self, request, *args, **kwargs):
        self._require_director_with_school()
        return super().destroy(request, *args, **kwargs)


class ClassRoomViewSet(DirectorWriteMixin, viewsets.ModelViewSet):
    serializer_class = ClassRoomSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ClassRoom.objects.none()

        if is_director(user) and user.school_id:
            queryset = ClassRoom.objects.filter(school=user.school)
        elif is_teacher(user):
            teacher = get_teacher_profile(user)
            if teacher:
                queryset = ClassRoom.objects.filter(
                    teacher_assignments__teacher=teacher,
                    school=user.school,
                )

        level = self.request.query_params.get('level')
        academic_year = self.request.query_params.get('academic_year')
        if level:
            queryset = queryset.filter(level=level)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        return queryset.distinct().order_by('level', 'name')


class SubjectViewSet(DirectorWriteMixin, viewsets.ModelViewSet):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Subject.objects.none()

        if is_director(user) and user.school_id:
            queryset = Subject.objects.filter(school=user.school)
        elif is_teacher(user):
            teacher = get_teacher_profile(user)
            if teacher:
                queryset = Subject.objects.filter(
                    teacher_assignments__teacher=teacher,
                    school=user.school,
                )

        return queryset.distinct().order_by('name')


class StudentViewSet(DirectorWriteMixin, viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Student.objects.none()

        if is_director(user) and user.school_id:
            queryset = Student.objects.filter(school=user.school)
        elif is_teacher(user):
            teacher = get_teacher_profile(user)
            if teacher:
                queryset = Student.objects.filter(
                    classroom__teacher_assignments__teacher=teacher,
                    school=user.school,
                )
        elif is_parent(user):
            parent = get_parent_profile(user)
            if parent:
                queryset = Student.objects.filter(
                    parent_relations__parent=parent,
                    school=user.school,
                )

        classroom_id = self.request.query_params.get('classroom_id')
        is_active = self.request.query_params.get('is_active')
        search = self.request.query_params.get('search')

        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if is_active is not None:
            queryset = queryset.filter(is_active=_boolean_query_value(is_active))
        if search:
            queryset = queryset.filter(
                Q(student_code__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
            )

        return queryset.distinct().order_by('last_name', 'first_name')

    def _validate_student_school(self, serializer):
        classroom = serializer.validated_data.get('classroom')
        if classroom and classroom.school_id != self.request.user.school_id:
            raise ValidationError('Classroom must belong to your school.')

    def perform_create(self, serializer):
        self._require_director_with_school()
        self._validate_student_school(serializer)
        serializer.save(school=self._user_school())

    def perform_update(self, serializer):
        self._require_director_with_school()
        self._validate_student_school(serializer)
        serializer.save(school=self._user_school())

    def destroy(self, request, *args, **kwargs):
        self._require_director_with_school()
        student = self.get_object()
        student.is_active = False
        student.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def deactivate(self, request, pk=None):
        self._require_director_with_school()
        student = self.get_object()
        student.is_active = False
        student.save(update_fields=['is_active'])
        serializer = self.get_serializer(student)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='attendance-calendar')
    def attendance_calendar(self, request, pk=None):
        from apps.attendance.models import AttendanceRecord
        from apps.attendance.serializers import AttendanceRecordSerializer

        student = self.get_object()
        queryset = AttendanceRecord.objects.filter(
            school=request.user.school,
            student=student,
        )

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if month:
            queryset = queryset.filter(date__month=month)
        if year:
            queryset = queryset.filter(date__year=year)

        serializer = AttendanceRecordSerializer(
            queryset.order_by('date', 'timetable_session__start_time'),
            many=True,
        )
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='current-status')
    def current_status(self, request, pk=None):
        from apps.attendance.models import AttendanceRecord

        student = self.get_object()
        today = timezone.localdate()
        current_time = timezone.localtime().time()
        day_of_week = today.strftime('%A').lower()

        session = TimetableSession.objects.filter(
            school=request.user.school,
            classroom=student.classroom,
            day_of_week=day_of_week,
            start_time__lte=current_time,
            end_time__gte=current_time,
        ).order_by('start_time').first()

        if session is None:
            return Response(
                {
                    'student_id': student.id,
                    'current_status': 'no_class_scheduled_now',
                    'session': None,
                }
            )

        attendance_record = AttendanceRecord.objects.filter(
            school=request.user.school,
            student=student,
            timetable_session=session,
            date=today,
        ).first()

        if attendance_record is None:
            current_status = 'attendance_not_marked_yet'
        elif attendance_record.status == AttendanceRecord.Status.PRESENT:
            current_status = 'present_now'
        elif attendance_record.status == AttendanceRecord.Status.ABSENT:
            current_status = 'absent_from_current_session'
        elif attendance_record.status == AttendanceRecord.Status.LATE:
            current_status = 'late'
        elif attendance_record.status == AttendanceRecord.Status.EXCUSED:
            current_status = 'excused'
        else:
            current_status = 'attendance_not_marked_yet'

        return Response(
            {
                'student_id': student.id,
                'current_status': current_status,
                'session': {
                    'id': session.id,
                    'subject': session.subject.name,
                    'start_time': session.start_time,
                    'end_time': session.end_time,
                },
            }
        )


class ParentStudentRelationViewSet(viewsets.ModelViewSet):
    serializer_class = ParentStudentRelationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if not is_director(user) or not user.school_id:
            return ParentStudentRelation.objects.none()
        return ParentStudentRelation.objects.filter(
            parent__school=user.school,
            student__school=user.school,
        ).order_by('student__last_name', 'student__first_name')

    def _require_director_with_school(self):
        if not is_director(self.request.user):
            raise PermissionDenied('Only directors can manage parent-student relations.')
        if not self.request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

    def _validate_relation_school(self, serializer):
        parent = serializer.validated_data.get('parent')
        student = serializer.validated_data.get('student')
        if parent and parent.school_id != self.request.user.school_id:
            raise ValidationError('Parent must belong to your school.')
        if student and student.school_id != self.request.user.school_id:
            raise ValidationError('Student must belong to your school.')

    def perform_create(self, serializer):
        self._require_director_with_school()
        self._validate_relation_school(serializer)
        serializer.save()

    def perform_update(self, serializer):
        self._require_director_with_school()
        self._validate_relation_school(serializer)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        self._require_director_with_school()
        return super().destroy(request, *args, **kwargs)


class TeacherClassAssignmentViewSet(DirectorWriteMixin, viewsets.ModelViewSet):
    serializer_class = TeacherClassAssignmentSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = TeacherClassAssignment.objects.none()

        if is_director(user) and user.school_id:
            queryset = TeacherClassAssignment.objects.filter(school=user.school)
        elif is_teacher(user):
            teacher = get_teacher_profile(user)
            if teacher:
                queryset = TeacherClassAssignment.objects.filter(
                    teacher=teacher,
                    school=user.school,
                )

        return queryset.order_by('classroom__name', 'subject__name')

    def _validate_assignment_school(self, serializer):
        teacher = serializer.validated_data.get('teacher')
        classroom = serializer.validated_data.get('classroom')
        subject = serializer.validated_data.get('subject')
        school_id = self.request.user.school_id

        if teacher and teacher.school_id != school_id:
            raise ValidationError('Teacher must belong to your school.')
        if classroom and classroom.school_id != school_id:
            raise ValidationError('Classroom must belong to your school.')
        if subject and subject.school_id != school_id:
            raise ValidationError('Subject must belong to your school.')

    def perform_create(self, serializer):
        self._require_director_with_school()
        self._validate_assignment_school(serializer)
        serializer.save(school=self._user_school())

    def perform_update(self, serializer):
        self._require_director_with_school()
        self._validate_assignment_school(serializer)
        serializer.save(school=self._user_school())


class TimetableSessionViewSet(DirectorWriteMixin, viewsets.ModelViewSet):
    serializer_class = TimetableSessionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = TimetableSession.objects.none()

        if is_director(user) and user.school_id:
            queryset = TimetableSession.objects.filter(school=user.school)
        elif is_teacher(user):
            teacher = get_teacher_profile(user)
            if teacher:
                queryset = TimetableSession.objects.filter(teacher=teacher, school=user.school)
        elif is_parent(user):
            parent = get_parent_profile(user)
            if parent:
                queryset = TimetableSession.objects.filter(
                    classroom__students__parent_relations__parent=parent,
                    school=user.school,
                )

        classroom_id = self.request.query_params.get('classroom_id')
        teacher_id = self.request.query_params.get('teacher_id')
        day_of_week = self.request.query_params.get('day_of_week')

        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)

        return queryset.distinct().order_by('day_of_week', 'start_time')

    def _validate_session_school(self, serializer):
        teacher = serializer.validated_data.get('teacher')
        classroom = serializer.validated_data.get('classroom')
        subject = serializer.validated_data.get('subject')
        school_id = self.request.user.school_id

        if teacher and teacher.school_id != school_id:
            raise ValidationError('Teacher must belong to your school.')
        if classroom and classroom.school_id != school_id:
            raise ValidationError('Classroom must belong to your school.')
        if subject and subject.school_id != school_id:
            raise ValidationError('Subject must belong to your school.')

    def perform_create(self, serializer):
        self._require_director_with_school()
        self._validate_session_school(serializer)
        serializer.save(school=self._user_school())

    def perform_update(self, serializer):
        self._require_director_with_school()
        self._validate_session_school(serializer)
        serializer.save(school=self._user_school())
