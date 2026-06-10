from rest_framework.permissions import SAFE_METHODS, BasePermission

from .access import (
    is_director,
    is_parent,
    is_teacher,
    parent_has_object_access,
    parent_has_student_access,
    same_school,
    teacher_has_class_access,
    teacher_has_object_access,
    teacher_has_session_access,
    teacher_has_student_access,
)


class IsDirector(BasePermission):
    """Allow only director users."""

    def has_permission(self, request, view):
        return is_director(request.user)


class IsTeacher(BasePermission):
    """Allow only teacher users."""

    def has_permission(self, request, view):
        return is_teacher(request.user)


class IsParent(BasePermission):
    """Allow only parent users."""

    def has_permission(self, request, view):
        return is_parent(request.user)


class IsDirectorOrReadOnly(BasePermission):
    """Allow read access to authenticated users, writes to directors only."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return is_director(request.user)

    def has_object_permission(self, request, view, obj):
        if not same_school(request.user, obj):
            return False
        if request.method in SAFE_METHODS:
            return True
        return is_director(request.user)


class IsSchoolMember(BasePermission):
    """Require an authenticated user connected to a school."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'school_id', None)
        )


class IsSameSchool(BasePermission):
    """Object must belong to the same school as the request user."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return same_school(request.user, obj)


class IsDirectorOfSchool(BasePermission):
    """Director can access objects in their own school only."""

    def has_permission(self, request, view):
        return is_director(request.user)

    def has_object_permission(self, request, view, obj):
        return is_director(request.user) and same_school(request.user, obj)


class IsAssignedTeacher(BasePermission):
    """Teacher can access assigned classes, sessions, and students only."""

    def has_permission(self, request, view):
        return is_teacher(request.user)

    def has_object_permission(self, request, view, obj):
        if not is_teacher(request.user) or not same_school(request.user, obj):
            return False

        if obj.__class__.__name__ == 'ClassRoom':
            return teacher_has_class_access(request.user, obj)
        if obj.__class__.__name__ == 'Student':
            return teacher_has_student_access(request.user, obj)
        if obj.__class__.__name__ == 'TimetableSession':
            return teacher_has_session_access(request.user, obj)
        return teacher_has_object_access(request.user, obj)


class IsParentOfStudent(BasePermission):
    """Parent can access linked students or records for linked students only."""

    def has_permission(self, request, view):
        return is_parent(request.user)

    def has_object_permission(self, request, view, obj):
        if not is_parent(request.user) or not same_school(request.user, obj):
            return False

        if obj.__class__.__name__ == 'Student':
            return parent_has_student_access(request.user, obj)
        return parent_has_object_access(request.user, obj)


class IsDirectorOrAssignedTeacher(BasePermission):
    """Director in same school or assigned teacher can access the object."""

    def has_permission(self, request, view):
        return is_director(request.user) or is_teacher(request.user)

    def has_object_permission(self, request, view, obj):
        if not same_school(request.user, obj):
            return False
        if is_director(request.user):
            return True
        return IsAssignedTeacher().has_object_permission(request, view, obj)


class IsDirectorOrParentOfStudent(BasePermission):
    """Director in same school or linked parent can access the object."""

    def has_permission(self, request, view):
        return is_director(request.user) or is_parent(request.user)

    def has_object_permission(self, request, view, obj):
        if not same_school(request.user, obj):
            return False
        if is_director(request.user):
            return True
        return IsParentOfStudent().has_object_permission(request, view, obj)


class IsDirectorOrAssignedTeacherOrParentOfStudent(BasePermission):
    """Director, assigned teacher, or linked parent can access the object."""

    def has_permission(self, request, view):
        return (
            is_director(request.user)
            or is_teacher(request.user)
            or is_parent(request.user)
        )

    def has_object_permission(self, request, view, obj):
        if not same_school(request.user, obj):
            return False
        if is_director(request.user):
            return True
        if is_teacher(request.user):
            return IsAssignedTeacher().has_object_permission(request, view, obj)
        return IsParentOfStudent().has_object_permission(request, view, obj)
