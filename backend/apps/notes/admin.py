from django.contrib import admin

from .models import TeacherNote


@admin.register(TeacherNote)
class TeacherNoteAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'teacher',
        'classroom',
        'note_type',
        'title',
        'created_at',
        'school',
    )
    list_filter = ('school', 'note_type', 'classroom', 'teacher')
    search_fields = (
        'student__first_name',
        'student__last_name',
        'title',
        'content',
    )
    ordering = ('-created_at',)
