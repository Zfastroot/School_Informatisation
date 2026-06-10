from rest_framework import serializers

from .models import AttendanceRecord


class AttendanceRecordSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    student_name = serializers.CharField(source='student', read_only=True)
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    session_label = serializers.CharField(source='timetable_session', read_only=True)
    marked_by_teacher_name = serializers.CharField(
        source='marked_by_teacher.user.full_name',
        read_only=True,
    )

    class Meta:
        model = AttendanceRecord
        fields = (
            'id',
            'school',
            'school_name',
            'student',
            'student_name',
            'student_code',
            'timetable_session',
            'session_label',
            'marked_by_teacher',
            'marked_by_teacher_name',
            'date',
            'status',
            'marked_at',
        )
        read_only_fields = ('id', 'school', 'marked_by_teacher', 'marked_at')


class AttendanceRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ('status',)


class AttendanceMarkRecordSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=AttendanceRecord.Status.choices)


class AttendanceMarkSerializer(serializers.Serializer):
    timetable_session_id = serializers.IntegerField()
    date = serializers.DateField()
    records = AttendanceMarkRecordSerializer(many=True)
