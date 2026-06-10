from django.db import models


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'
        EXCUSED = 'excused', 'Excused'
        NOT_MARKED = 'not_marked', 'Not marked'

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    student = models.ForeignKey(
        'academics.Student',
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    timetable_session = models.ForeignKey(
        'academics.TimetableSession',
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    marked_by_teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.PROTECT,
        related_name='marked_attendance_records',
    )
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_MARKED,
    )
    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'timetable_session', 'date'],
                name='unique_student_session_attendance_date',
            ),
        ]

    def __str__(self):
        return f'{self.student} - {self.timetable_session} - {self.date}'
