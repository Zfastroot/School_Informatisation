from rest_framework import serializers

from .models import (
    ClassRoom,
    ParentStudentRelation,
    Student,
    Subject,
    TeacherClassAssignment,
    TimetableSession,
)


class ClassRoomSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = ClassRoom
        fields = ('id', 'school', 'school_name', 'name', 'level', 'academic_year')
        read_only_fields = ('id', 'school')


class SubjectSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'school', 'school_name', 'name')
        read_only_fields = ('id', 'school')


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    school_name = serializers.CharField(source='school.name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)

    class Meta:
        model = Student
        fields = (
            'id',
            'school',
            'school_name',
            'classroom',
            'classroom_name',
            'student_code',
            'first_name',
            'last_name',
            'full_name',
            'date_of_birth',
            'gender',
            'is_active',
        )
        read_only_fields = ('id', 'school')

    def get_full_name(self, obj):
        return str(obj)


class ParentStudentRelationSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.user.full_name', read_only=True)
    parent_email = serializers.EmailField(source='parent.user.email', read_only=True)
    student_name = serializers.CharField(source='student', read_only=True)

    class Meta:
        model = ParentStudentRelation
        fields = (
            'id',
            'parent',
            'parent_name',
            'parent_email',
            'student',
            'student_name',
            'relationship',
        )


class TeacherClassAssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)
    teacher_email = serializers.EmailField(source='teacher.user.email', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = TeacherClassAssignment
        fields = (
            'id',
            'school',
            'school_name',
            'teacher',
            'teacher_name',
            'teacher_email',
            'classroom',
            'classroom_name',
            'subject',
            'subject_name',
        )
        read_only_fields = ('id', 'school')


class TimetableSessionSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)
    teacher_email = serializers.EmailField(source='teacher.user.email', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = TimetableSession
        fields = (
            'id',
            'school',
            'school_name',
            'classroom',
            'classroom_name',
            'teacher',
            'teacher_name',
            'teacher_email',
            'subject',
            'subject_name',
            'day_of_week',
            'start_time',
            'end_time',
        )
        read_only_fields = ('id', 'school')
