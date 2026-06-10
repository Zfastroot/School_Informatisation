from rest_framework import serializers

from .models import StudentPayment


class StudentPaymentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    student_name = serializers.CharField(source='student', read_only=True)
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = StudentPayment
        fields = (
            'id',
            'school',
            'school_name',
            'student',
            'student_id',
            'student_name',
            'student_code',
            'month',
            'year',
            'amount_due',
            'amount_paid',
            'status',
            'due_date',
        )
        read_only_fields = ('id', 'school', 'student')

    def create(self, validated_data):
        validated_data.pop('student_id', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('student_id', None)
        return super().update(instance, validated_data)
