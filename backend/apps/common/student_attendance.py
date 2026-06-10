from django.utils import timezone

from apps.academics.models import TimetableSession
from apps.attendance.models import AttendanceRecord


def get_student_current_status(student, school):
    today = timezone.localdate()
    current_time = timezone.localtime().time()
    day_of_week = today.strftime('%A').lower()

    session = TimetableSession.objects.filter(
        school=school,
        classroom=student.classroom,
        day_of_week=day_of_week,
        start_time__lte=current_time,
        end_time__gte=current_time,
    ).order_by('start_time').first()

    if session is None:
        return {
            'student_id': student.id,
            'current_status': 'no_class_scheduled_now',
            'session': None,
        }

    attendance_record = AttendanceRecord.objects.filter(
        school=school,
        student=student,
        timetable_session=session,
        date=today,
    ).first()

    if attendance_record is None:
        current_status = 'attendance_not_marked_yet'
    elif attendance_record.status == AttendanceRecord.Status.PRESENT:
        current_status = 'present_now'
    elif attendance_record.status == AttendanceRecord.Status.ABSENT:
        current_status = 'absent_from_current_session'
    elif attendance_record.status == AttendanceRecord.Status.LATE:
        current_status = 'late'
    elif attendance_record.status == AttendanceRecord.Status.EXCUSED:
        current_status = 'excused'
    else:
        current_status = 'attendance_not_marked_yet'

    return {
        'student_id': student.id,
        'current_status': current_status,
        'session': {
            'id': session.id,
            'subject': session.subject.name,
            'start_time': session.start_time,
            'end_time': session.end_time,
        },
    }
