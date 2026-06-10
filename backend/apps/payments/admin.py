from django.contrib import admin

from .models import StudentPayment


@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'month',
        'year',
        'amount_due',
        'amount_paid',
        'status',
        'due_date',
        'school',
    )
    list_filter = ('school', 'status', 'month', 'year')
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__student_code',
    )
    ordering = ('-year', '-month', 'student__last_name')
