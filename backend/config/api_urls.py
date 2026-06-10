from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.academics.views import (
    ClassRoomViewSet,
    ParentStudentRelationViewSet,
    StudentViewSet,
    SubjectViewSet,
    TeacherClassAssignmentViewSet,
    TimetableSessionViewSet,
)
from apps.accounts.views import UserViewSet
from apps.attendance.views import AttendanceRecordViewSet
from apps.dashboard.views import (
    DirectorDashboardView,
    ParentChildAttendanceCalendarView,
    ParentChildCurrentStatusView,
    ParentChildTodayAttendanceView,
    ParentChildrenView,
    TeacherDashboardView,
)
from apps.notes.views import TeacherNoteViewSet
from apps.payments.views import StudentPaymentViewSet
from apps.schools.views import SchoolView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('classes', ClassRoomViewSet, basename='class')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('students', StudentViewSet, basename='student')
router.register(
    'parent-student-relations',
    ParentStudentRelationViewSet,
    basename='parent-student-relation',
)
router.register(
    'teacher-class-assignments',
    TeacherClassAssignmentViewSet,
    basename='teacher-class-assignment',
)
router.register(
    'timetable-sessions',
    TimetableSessionViewSet,
    basename='timetable-session',
)
router.register('attendance', AttendanceRecordViewSet, basename='attendance')
router.register('teacher-notes', TeacherNoteViewSet, basename='teacher-note')
router.register('payments', StudentPaymentViewSet, basename='payment')

urlpatterns = [
    path('school/', SchoolView.as_view(), name='school'),
    path('dashboard/director/', DirectorDashboardView.as_view(), name='dashboard-director'),
    path('dashboard/teacher/', TeacherDashboardView.as_view(), name='dashboard-teacher'),
    path('parent/children/', ParentChildrenView.as_view(), name='parent-children'),
    path(
        'parent/children/<int:student_id>/today-attendance/',
        ParentChildTodayAttendanceView.as_view(),
        name='parent-child-today-attendance',
    ),
    path(
        'parent/children/<int:student_id>/attendance-calendar/',
        ParentChildAttendanceCalendarView.as_view(),
        name='parent-child-attendance-calendar',
    ),
    path(
        'parent/children/<int:student_id>/current-status/',
        ParentChildCurrentStatusView.as_view(),
        name='parent-child-current-status',
    ),
    path('', include(router.urls)),
]
