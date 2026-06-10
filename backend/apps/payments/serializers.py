from rest_framework import serializers

from .models import StudentPayment


class StudentPaymentSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    student_name = serializers.CharField(source='student', read_only=True)
    student_code = serializers.CharField(source='student.student_code', read_only=True)

    class Meta:
        model = StudentPayment
        fields = (
            'id',
            'school',
            'school_name',
            'student',
            'student_name',
            'student_code',
            'month',
            'year',
            'amount_due',
            'amount_paid',
            'status',
            'due_date',
        )
