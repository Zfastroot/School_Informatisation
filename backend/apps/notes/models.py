from django.db import models


class TeacherNote(models.Model):
    class NoteType(models.TextChoices):
        BEHAVIOR = 'behavior', 'Behavior'
        HOMEWORK = 'homework', 'Homework'
        PERFORMANCE = 'performance', 'Performance'
        DISCIPLINE = 'discipline', 'Discipline'
        GENERAL = 'general', 'General'

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='teacher_notes',
    )
    student = models.ForeignKey(
        'academics.Student',
        on_delete=models.CASCADE,
        related_name='teacher_notes',
    )
    teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.CASCADE,
        related_name='teacher_notes',
    )
    classroom = models.ForeignKey(
        'academics.ClassRoom',
        on_delete=models.CASCADE,
        related_name='teacher_notes',
    )
    note_type = models.CharField(
        max_length=20,
        choices=NoteType.choices,
        default=NoteType.GENERAL,
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} - {self.title}'
