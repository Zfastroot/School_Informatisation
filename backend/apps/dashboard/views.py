from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.academics.models import ClassRoom, Student, TimetableSession
from apps.attendance.models import AttendanceRecord
from apps.attendance.serializers import AttendanceRecordSerializer
from apps.common.access import (
    get_parent_profile,
    get_teacher_profile,
    is_director,
    is_parent,
    is_teacher,
    parent_has_student_access,
)
from apps.common.student_attendance import get_student_current_status
from apps.notes.models import TeacherNote
from apps.payments.models import StudentPayment


def _today_context():
    today = timezone.localdate()
    return today, today.strftime('%A').lower(), timezone.localtime().time()


class DirectorDashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not is_director(request.user):
            raise PermissionDenied('Only directors can access this dashboard.')
        if not request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

        school = request.user.school
        today, day_of_week, _current_time = _today_context()
        today_attendance = AttendanceRecord.objects.filter(school=school, date=today)
        today_sessions = TimetableSession.objects.filter(school=school, day_of_week=day_of_week)
        payments = StudentPayment.objects.filter(school=school)

        latest_notes = TeacherNote.objects.filter(school=school).order_by('-created_at')[:5]
        class_overview = []
        for classroom in ClassRoom.objects.filter(school=school).order_by('level', 'name'):
            class_sessions = today_sessions.filter(classroom=classroom)
            class_overview.append(
                {
                    'classroom_id': classroom.id,
                    'classroom_name': classroom.name,
                    'total_students': classroom.students.count(),
                    'attendance_marked_today': bool(
                        class_sessions.exists()
                        and not class_sessions.exclude(attendance_records__date=today).exists()
                    ),
                }
            )

        return Response(
            {
                'total_students': Student.objects.filter(school=school).count(),
                'today_attendance': {
                    'present': today_attendance.filter(
                        status=AttendanceRecord.Status.PRESENT,
                    ).count(),
                    'absent': today_attendance.filter(
                        status=AttendanceRecord.Status.ABSENT,
                    ).count(),
                    'late': today_attendance.filter(status=AttendanceRecord.Status.LATE).count(),
                    'excused': today_attendance.filter(
                        status=AttendanceRecord.Status.EXCUSED,
                    ).count(),
                    'not_marked_sessions': today_sessions.exclude(
                        attendance_records__date=today,
                    ).distinct().count(),
                },
                'absent_students_count': today_attendance.filter(
                    status=AttendanceRecord.Status.ABSENT,
                ).count(),
                'late_students_count': today_attendance.filter(
                    status=AttendanceRecord.Status.LATE,
                ).count(),
                'attendance_not_marked_sessions_count': today_sessions.exclude(
                    attendance_records__date=today,
                ).distinct().count(),
                'payments': {
                    'paid_students': payments.filter(status=StudentPayment.Status.PAID).count(),
                    'unpaid_students': payments.filter(status=StudentPayment.Status.UNPAID).count(),
                    'partial_students': payments.filter(
                        status=StudentPayment.Status.PARTIAL,
                    ).count(),
                    'late_students': payments.filter(status=StudentPayment.Status.LATE).count(),
                },
                'unpaid_students_count': payments.filter(
                    status=StudentPayment.Status.UNPAID,
                ).count(),
                'latest_teacher_notes': [
                    {
                        'id': note.id,
                        'student_name': str(note.student),
                        'teacher_name': note.teacher.user.full_name,
                        'note_type': note.note_type,
                        'title': note.title,
                        'created_at': note.created_at,
                    }
                    for note in latest_notes
                ],
                'class_overview': class_overview,
            }
        )


class TeacherDashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not is_teacher(request.user):
            raise PermissionDenied('Only teachers can access this dashboard.')
        if not request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

        teacher = get_teacher_profile(request.user)
        if teacher is None:
            raise PermissionDenied('Teacher profile was not found.')

        today, day_of_week, _current_time = _today_context()
        today_sessions = TimetableSession.objects.filter(
            school=request.user.school,
            teacher=teacher,
            day_of_week=day_of_week,
        ).order_by('start_time')
        assigned_classes = ClassRoom.objects.filter(
            school=request.user.school,
            teacher_assignments__teacher=teacher,
        ).distinct().order_by('level', 'name')

        return Response(
            {
                'today_sessions': [
                    {
                        'id': session.id,
                        'classroom': session.classroom.name,
                        'subject': session.subject.name,
                        'start_time': session.start_time,
                        'end_time': session.end_time,
                        'attendance_marked': session.attendance_records.filter(
                            date=today,
                        ).exists(),
                    }
                    for session in today_sessions
                ],
                'assigned_classes': [
                    {
                        'id': classroom.id,
                        'name': classroom.name,
                    }
                    for classroom in assigned_classes
                ],
            }
        )


class ParentChildrenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        parent = _get_parent_or_error(request.user)
        students = Student.objects.filter(
            school=request.user.school,
            parent_relations__parent=parent,
        ).distinct().order_by('last_name', 'first_name')
        return Response(
            [
                {
                    'id': student.id,
                    'full_name': str(student),
                    'classroom': student.classroom.name,
                }
                for student in students
            ]
        )


class ParentChildTodayAttendanceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, student_id):
        student = _get_parent_child_or_error(request.user, student_id)
        today, day_of_week, _current_time = _today_context()
        sessions = TimetableSession.objects.filter(
            school=request.user.school,
            classroom=student.classroom,
            day_of_week=day_of_week,
        ).order_by('start_time')

        return Response(
            {
                'student_id': student.id,
                'date': today,
                'sessions': [
                    _parent_session_attendance_payload(student, session, today)
                    for session in sessions
                ],
            }
        )


class ParentChildAttendanceCalendarView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, student_id):
        student = _get_parent_child_or_error(request.user, student_id)
        queryset = AttendanceRecord.objects.filter(
            school=request.user.school,
            student=student,
        )

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if month:
            queryset = queryset.filter(date__month=month)
        if year:
            queryset = queryset.filter(date__year=year)

        serializer = AttendanceRecordSerializer(
            queryset.order_by('date', 'timetable_session__start_time'),
            many=True,
        )
        return Response(serializer.data)


class ParentChildCurrentStatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, student_id):
        student = _get_parent_child_or_error(request.user, student_id)
        return Response(get_student_current_status(student, request.user.school))


def _get_parent_or_error(user):
    if not is_parent(user):
        raise PermissionDenied('Only parents can access this endpoint.')
    if not user.school_id:
        raise PermissionDenied('Your account is not connected to a school.')
    parent = get_parent_profile(user)
    if parent is None:
        raise PermissionDenied('Parent profile was not found.')
    return parent


def _get_parent_child_or_error(user, student_id):
    _get_parent_or_error(user)
    student = Student.objects.filter(id=student_id, school=user.school).first()
    if student is None or not parent_has_student_access(user, student):
        raise PermissionDenied('You can access only your own children.')
    return student


def _parent_session_attendance_payload(student, session, date):
    attendance_record = AttendanceRecord.objects.filter(
        school=student.school,
        student=student,
        timetable_session=session,
        date=date,
    ).first()
    return {
        'time': f'{session.start_time:%H:%M}-{session.end_time:%H:%M}',
        'subject': session.subject.name,
        'status': attendance_record.status if attendance_record else 'not_marked',
    }
