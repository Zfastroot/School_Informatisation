from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.academics.models import TimetableSession
from apps.common.access import (
    get_parent_profile,
    get_teacher_profile,
    is_director,
    is_parent,
    is_teacher,
    teacher_has_session_access,
)

from .models import AttendanceRecord
from .serializers import (
    AttendanceMarkSerializer,
    AttendanceRecordSerializer,
    AttendanceRecordUpdateSerializer,
)


class AttendanceRecordViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'patch', 'post', 'head', 'options')

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AttendanceRecordUpdateSerializer
        return AttendanceRecordSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = AttendanceRecord.objects.none()

        if is_director(user) and user.school_id:
            queryset = AttendanceRecord.objects.filter(school=user.school)
        elif is_teacher(user):
            teacher = get_teacher_profile(user)
            if teacher:
                queryset = AttendanceRecord.objects.filter(
                    timetable_session__teacher=teacher,
                    school=user.school,
                )
        elif is_parent(user):
            parent = get_parent_profile(user)
            if parent:
                queryset = AttendanceRecord.objects.filter(
                    student__parent_relations__parent=parent,
                    school=user.school,
                )

        date = self.request.query_params.get('date')
        student_id = self.request.query_params.get('student_id')
        classroom_id = self.request.query_params.get('classroom_id')
        timetable_session_id = self.request.query_params.get('timetable_session_id')
        attendance_status = self.request.query_params.get('status')

        if date:
            queryset = queryset.filter(date=date)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if classroom_id:
            queryset = queryset.filter(student__classroom_id=classroom_id)
        if timetable_session_id:
            queryset = queryset.filter(timetable_session_id=timetable_session_id)
        if attendance_status:
            queryset = queryset.filter(status=attendance_status)

        return queryset.distinct().order_by('-date', 'student__last_name', 'student__first_name')

    def _get_session_for_marking(self, timetable_session_id):
        user = self.request.user
        try:
            session = TimetableSession.objects.get(
                id=timetable_session_id,
                school=user.school,
            )
        except TimetableSession.DoesNotExist as exc:
            raise ValidationError('Timetable session was not found in your school.') from exc

        if is_director(user):
            return session
        if is_teacher(user) and teacher_has_session_access(user, session):
            return session
        raise PermissionDenied('You cannot mark attendance for this session.')

    def _get_marker_teacher(self, session):
        if is_teacher(self.request.user):
            return get_teacher_profile(self.request.user)
        return session.teacher

    def partial_update(self, request, *args, **kwargs):
        record = self.get_object()
        if is_parent(request.user):
            raise PermissionDenied('Parents cannot update attendance.')
        if is_teacher(request.user) and not teacher_has_session_access(
            request.user,
            record.timetable_session,
        ):
            raise PermissionDenied('You cannot update attendance for this session.')
        return super().partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        record = self.get_object()
        serializer.save(
            school=record.school,
            student=record.student,
            timetable_session=record.timetable_session,
            marked_by_teacher=self._get_marker_teacher(record.timetable_session),
        )

    @action(detail=False, methods=['post'])
    def mark(self, request):
        serializer = AttendanceMarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = self._get_session_for_marking(
            serializer.validated_data['timetable_session_id'],
        )
        marker_teacher = self._get_marker_teacher(session)
        attendance_date = serializer.validated_data['date']
        saved_records = []

        for record_data in serializer.validated_data['records']:
            student_id = record_data['student_id']
            attendance_status = record_data['status']
            student = session.classroom.students.filter(
                id=student_id,
                school=session.school,
            ).first()
            if student is None:
                raise ValidationError(
                    f'Student {student_id} does not belong to the session classroom.'
                )

            attendance_record, _created = AttendanceRecord.objects.update_or_create(
                student=student,
                timetable_session=session,
                date=attendance_date,
                defaults={
                    'school': session.school,
                    'marked_by_teacher': marker_teacher,
                    'status': attendance_status,
                },
            )
            saved_records.append(attendance_record)

        return Response(
            {
                'message': 'Attendance saved successfully',
                'timetable_session_id': session.id,
                'date': attendance_date,
                'total_records': len(saved_records),
            },
            status=status.HTTP_200_OK,
        )
