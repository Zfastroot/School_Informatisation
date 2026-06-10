from django.db import models


class ClassRoom(models.Model):
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='classrooms',
    )
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Subject(models.Model):
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='subjects',
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='students',
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.PROTECT,
        related_name='students',
    )
    student_code = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ParentStudentRelation(models.Model):
    parent = models.ForeignKey(
        'accounts.ParentProfile',
        on_delete=models.CASCADE,
        related_name='student_relations',
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='parent_relations',
    )
    relationship = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'student'],
                name='unique_parent_student_relation',
            ),
        ]

    def __str__(self):
        return f'{self.parent} - {self.student}'


class TeacherClassAssignment(models.Model):
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='teacher_class_assignments',
    )
    teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.CASCADE,
        related_name='class_assignments',
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='teacher_assignments',
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='teacher_assignments',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'classroom', 'subject'],
                name='unique_teacher_class_subject_assignment',
            ),
        ]

    def __str__(self):
        return f'{self.teacher} - {self.classroom} - {self.subject}'


class TimetableSession(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='timetable_sessions',
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='timetable_sessions',
    )
    teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.CASCADE,
        related_name='timetable_sessions',
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='timetable_sessions',
    )
    day_of_week = models.CharField(max_length=20, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.classroom} - {self.subject} - {self.day_of_week}'
