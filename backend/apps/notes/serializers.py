from rest_framework import serializers

from .models import TeacherNote


class TeacherNoteSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    student_name = serializers.CharField(source='student', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)

    class Meta:
        model = TeacherNote
        fields = (
            'id',
            'school',
            'school_name',
            'student',
            'student_name',
            'teacher',
            'teacher_name',
            'classroom',
            'classroom_name',
            'note_type',
            'title',
            'content',
            'created_at',
        )
        read_only_fields = ('created_at',)
