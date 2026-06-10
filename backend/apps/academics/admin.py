from django.contrib import admin

from .models import (
    ClassRoom,
    ParentStudentRelation,
    Student,
    Subject,
    TeacherClassAssignment,
    TimetableSession,
)


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'academic_year', 'school')
    list_filter = ('school', 'level', 'academic_year')
    search_fields = ('name', 'level', 'academic_year')
    ordering = ('school', 'level', 'name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    list_filter = ('school',)
    search_fields = ('name',)
    ordering = ('school', 'name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_code',
        'first_name',
        'last_name',
        'classroom',
        'school',
        'gender',
        'is_active',
    )
    list_filter = ('school', 'classroom', 'gender', 'is_active')
    search_fields = ('student_code', 'first_name', 'last_name')
    ordering = ('school', 'classroom', 'last_name', 'first_name')


@admin.register(ParentStudentRelation)
class ParentStudentRelationAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'relationship')
    list_filter = ('relationship',)
    search_fields = (
        'parent__user__full_name',
        'parent__user__email',
        'student__first_name',
        'student__last_name',
    )
    ordering = ('parent__user__full_name', 'student__last_name')


@admin.register(TeacherClassAssignment)
class TeacherClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'classroom', 'subject', 'school')
    list_filter = ('school', 'classroom', 'subject')
    search_fields = (
        'teacher__user__full_name',
        'teacher__user__email',
        'classroom__name',
        'subject__name',
    )
    ordering = ('school', 'classroom', 'subject')


@admin.register(TimetableSession)
class TimetableSessionAdmin(admin.ModelAdmin):
    list_display = (
        'classroom',
        'subject',
        'teacher',
        'day_of_week',
        'start_time',
        'end_time',
        'school',
    )
    list_filter = ('school', 'classroom', 'subject', 'teacher', 'day_of_week')
    search_fields = (
        'classroom__name',
        'subject__name',
        'teacher__user__full_name',
        'teacher__user__email',
    )
    ordering = ('school', 'day_of_week', 'start_time')
