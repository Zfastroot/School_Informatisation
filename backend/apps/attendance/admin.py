from django.contrib import admin

from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'timetable_session',
        'status',
        'date',
        'marked_by_teacher',
        'marked_at',
        'school',
    )
    list_filter = ('school', 'status', 'date', 'timetable_session')
    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__student_code',
    )
    ordering = ('-date', 'student__last_name')
