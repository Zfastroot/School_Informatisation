from django.db import models


class StudentPayment(models.Model):
    class Status(models.TextChoices):
        PAID = 'paid', 'Paid'
        UNPAID = 'unpaid', 'Unpaid'
        PARTIAL = 'partial', 'Partial'
        LATE = 'late', 'Late'

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='student_payments',
    )
    student = models.ForeignKey(
        'academics.Student',
        on_delete=models.CASCADE,
        related_name='payments',
    )
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UNPAID,
    )
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'month', 'year'],
                name='unique_student_payment_month_year',
            ),
        ]

    def __str__(self):
        return f'{self.student} - {self.month}/{self.year}'
