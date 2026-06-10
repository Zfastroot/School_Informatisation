from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.academics.models import ClassRoom, Student
from apps.accounts.models import TeacherProfile
from apps.common.access import (
    get_teacher_profile,
    is_director,
    is_parent,
    is_teacher,
)

from .models import TeacherNote
from .serializers import TeacherNoteSerializer


class TeacherNoteViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherNoteSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_queryset(self):
        user = self.request.user
        if is_parent(user):
            raise PermissionDenied('Parents cannot access teacher notes in the MVP.')

        queryset = TeacherNote.objects.none()

        if is_director(user) and user.school_id:
            queryset = TeacherNote.objects.filter(school=user.school)
        elif is_teacher(user):
            teacher = get_teacher_profile(user)
            if teacher:
                queryset = TeacherNote.objects.filter(
                    Q(teacher=teacher)
                    | Q(student__classroom__teacher_assignments__teacher=teacher),
                    school=user.school,
                )

        student_id = self.request.query_params.get('student_id')
        teacher_id = self.request.query_params.get('teacher_id')
        classroom_id = self.request.query_params.get('classroom_id')
        note_type = self.request.query_params.get('note_type')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if note_type:
            queryset = queryset.filter(note_type=note_type)

        return queryset.distinct().order_by('-created_at')

    def _require_school_member(self):
        if is_parent(self.request.user):
            raise PermissionDenied('Parents cannot access teacher notes in the MVP.')
        if not (is_director(self.request.user) or is_teacher(self.request.user)):
            raise PermissionDenied('You cannot access teacher notes.')
        if not self.request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

    def _get_student_and_classroom(self, serializer, instance=None):
        student_id = serializer.validated_data.get('student_id')
        classroom_id = serializer.validated_data.get('classroom_id')

        if instance is None and (not student_id or not classroom_id):
            raise ValidationError('student_id and classroom_id are required.')

        student = instance.student if instance and not student_id else None
        classroom = instance.classroom if instance and not classroom_id else None

        if student_id:
            student = Student.objects.filter(
                id=student_id,
                school=self.request.user.school,
            ).first()
        if classroom_id:
            classroom = ClassRoom.objects.filter(
                id=classroom_id,
                school=self.request.user.school,
            ).first()

        if student is None:
            raise ValidationError('Student was not found in your school.')
        if classroom is None:
            raise ValidationError('Classroom was not found in your school.')
        if student.classroom_id != classroom.id:
            raise ValidationError('Student must belong to the selected classroom.')

        return student, classroom

    def _get_note_teacher(self, serializer, classroom, instance=None):
        if is_teacher(self.request.user):
            teacher = get_teacher_profile(self.request.user)
            if not teacher:
                raise PermissionDenied('Teacher profile was not found.')
            if not teacher.class_assignments.filter(classroom=classroom).exists():
                raise PermissionDenied('You cannot create notes for this classroom.')
            return teacher

        teacher_id = serializer.validated_data.get('teacher_id')
        if instance and not teacher_id:
            teacher = instance.teacher
        elif teacher_id:
            teacher = TeacherProfile.objects.filter(
                id=teacher_id,
                school=self.request.user.school,
            ).first()
        else:
            raise ValidationError('teacher_id is required when a director creates a note.')

        if teacher is None:
            raise ValidationError('Teacher was not found in your school.')
        if not teacher.class_assignments.filter(classroom=classroom).exists():
            raise ValidationError('Teacher must be assigned to the selected classroom.')

        return teacher

    def perform_create(self, serializer):
        self._require_school_member()
        student, classroom = self._get_student_and_classroom(serializer)
        teacher = self._get_note_teacher(serializer, classroom)
        serializer.save(
            school=self.request.user.school,
            student=student,
            teacher=teacher,
            classroom=classroom,
        )

    def perform_update(self, serializer):
        self._require_school_member()
        note = self.get_object()
        if is_teacher(self.request.user) and note.teacher != get_teacher_profile(self.request.user):
            raise PermissionDenied('Teachers can update only their own notes.')

        student, classroom = self._get_student_and_classroom(serializer, instance=note)
        teacher = self._get_note_teacher(serializer, classroom, instance=note)
        serializer.save(
            school=note.school,
            student=student,
            teacher=teacher,
            classroom=classroom,
        )

    def destroy(self, request, *args, **kwargs):
        self._require_school_member()
        note = self.get_object()
        if is_teacher(request.user) and note.teacher != get_teacher_profile(request.user):
            raise PermissionDenied('Teachers can delete only their own notes.')
        return super().destroy(request, *args, **kwargs)
