from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import DirectorProfile, ParentProfile, TeacherProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('full_name', 'email', 'phone', 'role', 'school', 'is_active')
    list_filter = ('role', 'is_active', 'school')
    search_fields = ('full_name', 'email', 'phone', 'username')
    ordering = ('full_name',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('School profile', {'fields': ('full_name', 'phone', 'role', 'school')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('School profile', {'fields': ('full_name', 'email', 'phone', 'role', 'school')}),
    )


@admin.register(DirectorProfile)
class DirectorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school')
    list_filter = ('school',)
    search_fields = ('user__full_name', 'user__email', 'school__name')
    ordering = ('user__full_name',)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'employee_code')
    list_filter = ('school',)
    search_fields = ('user__full_name', 'user__email', 'employee_code')
    ordering = ('user__full_name',)


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'address')
    list_filter = ('school',)
    search_fields = ('user__full_name', 'user__email', 'address')
    ordering = ('user__full_name',)
