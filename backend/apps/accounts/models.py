from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        DIRECTOR = 'director', 'Director'
        TEACHER = 'teacher', 'Teacher'
        PARENT = 'parent', 'Parent'

    school = models.ForeignKey(
        'schools.School',
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DIRECTOR)

    def __str__(self):
        return self.full_name or self.username


class DirectorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='director_profile',
    )
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='director_profiles',
    )

    def __str__(self):
        return self.user.full_name


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
    )
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='teacher_profiles',
    )
    employee_code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.full_name


class ParentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent_profile',
    )
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.CASCADE,
        related_name='parent_profiles',
    )
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.full_name
