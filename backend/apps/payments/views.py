from decimal import Decimal

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.academics.models import Student
from apps.common.access import is_director

from .models import StudentPayment
from .serializers import StudentPaymentSerializer


def _money_string(value):
    return str((value or Decimal('0.00')).quantize(Decimal('0.01')))


class StudentPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentPaymentSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def _require_director_with_school(self):
        if not is_director(self.request.user):
            raise PermissionDenied('Only directors can access payments.')
        if not self.request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

    def get_queryset(self):
        self._require_director_with_school()
        queryset = StudentPayment.objects.filter(school=self.request.user.school)

        student_id = self.request.query_params.get('student_id')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        payment_status = self.request.query_params.get('status')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if month:
            queryset = queryset.filter(month=month)
        if year:
            queryset = queryset.filter(year=year)
        if payment_status:
            queryset = queryset.filter(status=payment_status)

        return queryset.order_by('-year', '-month', 'student__last_name', 'student__first_name')

    def _get_student(self, serializer, instance=None):
        student_id = serializer.validated_data.get('student_id')

        if instance is None and not student_id:
            raise ValidationError('student_id is required.')
        if instance and not student_id:
            return instance.student

        student = Student.objects.filter(
            id=student_id,
            school=self.request.user.school,
        ).first()
        if student is None:
            raise ValidationError('Student was not found in your school.')
        return student

    def _validate_unique_payment(self, serializer, student, instance=None):
        month = serializer.validated_data.get(
            'month',
            instance.month if instance else None,
        )
        year = serializer.validated_data.get(
            'year',
            instance.year if instance else None,
        )
        if month is None or year is None:
            return

        queryset = StudentPayment.objects.filter(
            student=student,
            month=month,
            year=year,
        )
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        if queryset.exists():
            raise ValidationError(
                'A payment record already exists for this student, month, and year.'
            )

    def perform_create(self, serializer):
        self._require_director_with_school()
        student = self._get_student(serializer)
        self._validate_unique_payment(serializer, student)
        serializer.save(school=self.request.user.school, student=student)

    def perform_update(self, serializer):
        self._require_director_with_school()
        payment = self.get_object()
        student = self._get_student(serializer, instance=payment)
        self._validate_unique_payment(serializer, student, instance=payment)
        serializer.save(school=payment.school, student=student)

    def destroy(self, request, *args, **kwargs):
        self._require_director_with_school()
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        self._require_director_with_school()
        queryset = StudentPayment.objects.filter(school=request.user.school)

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if month:
            queryset = queryset.filter(month=month)
        if year:
            queryset = queryset.filter(year=year)

        totals = queryset.aggregate(
            total_amount_due=Sum('amount_due'),
            total_amount_paid=Sum('amount_paid'),
        )

        return Response(
            {
                'month': int(month) if month else None,
                'year': int(year) if year else None,
                'paid_students': queryset.filter(status=StudentPayment.Status.PAID).count(),
                'unpaid_students': queryset.filter(status=StudentPayment.Status.UNPAID).count(),
                'partial_students': queryset.filter(status=StudentPayment.Status.PARTIAL).count(),
                'late_students': queryset.filter(status=StudentPayment.Status.LATE).count(),
                'total_amount_due': _money_string(totals['total_amount_due']),
                'total_amount_paid': _money_string(totals['total_amount_paid']),
            }
        )
