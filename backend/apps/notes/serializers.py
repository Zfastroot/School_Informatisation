from rest_framework import serializers

from .models import TeacherNote


class TeacherNoteSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    student_name = serializers.CharField(source='student', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.full_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    student_id = serializers.IntegerField(write_only=True, required=False)
    classroom_id = serializers.IntegerField(write_only=True, required=False)
    teacher_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = TeacherNote
        fields = (
            'id',
            'school',
            'school_name',
            'student',
            'student_id',
            'student_name',
            'teacher',
            'teacher_id',
            'teacher_name',
            'classroom',
            'classroom_id',
            'classroom_name',
            'note_type',
            'title',
            'content',
            'created_at',
        )
        read_only_fields = ('id', 'school', 'student', 'teacher', 'classroom', 'created_at')

    def create(self, validated_data):
        validated_data.pop('student_id', None)
        validated_data.pop('classroom_id', None)
        validated_data.pop('teacher_id', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('student_id', None)
        validated_data.pop('classroom_id', None)
        validated_data.pop('teacher_id', None)
        return super().update(instance, validated_data)
