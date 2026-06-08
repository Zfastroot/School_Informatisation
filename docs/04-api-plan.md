# API Plan Document — School Management Platform MVP

## 1. Purpose

This document defines the API plan for the School Management Platform MVP.

The goal is to help the backend development stay organized and API-first.

The backend should expose clean REST API endpoints that can be used by:

* Web dashboard
* Future Flutter mobile app
* Future parent/teacher mobile interfaces

The API should follow the MVP scope, user journey, and entity relationship documents.

Related documents:

* `docs/01-mvp-scope.md`
* `docs/02-user-journey.md`
* `docs/03-entities-relationships.md`

---

## 2. API Style

The MVP backend should use:

* Django
* Django REST Framework
* SQLite for local MVP development
* JWT authentication if authentication is implemented in the MVP
* JSON request and response format
* Role-based access control

Base API path:

```txt
/api/v1/
```

Example endpoint:

```txt
/api/v1/students/
```

---

## 3. Authentication API

### 3.1 Login

Endpoint:

```txt
POST /api/v1/auth/login/
```

Purpose:

Allow Director, Teacher, and Parent users to log in.

Request example:

```json
{
  "email_or_phone": "admin@school.com",
  "password": "password123"
}
```

Response example:

```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "user": {
    "id": 1,
    "full_name": "School Director",
    "role": "director",
    "school_id": 1
  }
}
```

---

### 3.2 Refresh Token

Endpoint:

```txt
POST /api/v1/auth/refresh/
```

Purpose:

Refresh the access token.

Request example:

```json
{
  "refresh": "jwt_refresh_token"
}
```

---

### 3.3 Current User

Endpoint:

```txt
GET /api/v1/auth/me/
```

Purpose:

Return the logged-in user profile and role.

Access:

* Director
* Teacher
* Parent

Response example:

```json
{
  "id": 1,
  "full_name": "School Director",
  "email": "admin@school.com",
  "phone": "0600000000",
  "role": "director",
  "school_id": 1
}
```

---

## 4. School API

### 4.1 Get School Information

Endpoint:

```txt
GET /api/v1/school/
```

Purpose:

Get the current user’s school information.

Access:

* Director
* Teacher
* Parent

Response example:

```json
{
  "id": 1,
  "name": "Al Amal Private School",
  "city": "Benslimane",
  "address": "Main Street",
  "phone": "0523000000"
}
```

---

### 4.2 Update School Information

Endpoint:

```txt
PATCH /api/v1/school/
```

Purpose:

Update school information.

Access:

* Director only

---

## 5. User Management API

### 5.1 List Users

Endpoint:

```txt
GET /api/v1/users/
```

Purpose:

List users inside the director’s school.

Access:

* Director only

---

### 5.2 Create User

Endpoint:

```txt
POST /api/v1/users/
```

Purpose:

Create teacher, parent, or director user accounts.

Access:

* Director only

Request example:

```json
{
  "full_name": "Mr. Yassine",
  "email": "yassine@school.com",
  "phone": "0611111111",
  "password": "password123",
  "role": "teacher"
}
```

---

### 5.3 Get User Details

Endpoint:

```txt
GET /api/v1/users/{id}/
```

Purpose:

View user details.

Access:

* Director only

---

### 5.4 Update User

Endpoint:

```txt
PATCH /api/v1/users/{id}/
```

Purpose:

Update user information.

Access:

* Director only

---

### 5.5 Deactivate User

Endpoint:

```txt
PATCH /api/v1/users/{id}/deactivate/
```

Purpose:

Deactivate a user account without deleting historical data.

Access:

* Director only

---

## 6. ClassRoom API

### 6.1 List Classes

Endpoint:

```txt
GET /api/v1/classes/
```

Purpose:

List classes.

Access:

* Director: all classes in the school
* Teacher: assigned classes only
* Parent: no direct access unless needed through child information

---

### 6.2 Create Class

Endpoint:

```txt
POST /api/v1/classes/
```

Purpose:

Create a class.

Access:

* Director only

Request example:

```json
{
  "name": "2AC A",
  "level": "2AC",
  "academic_year": "2026-2027"
}
```

---

### 6.3 Get Class Details

Endpoint:

```txt
GET /api/v1/classes/{id}/
```

Purpose:

View class information and students.

Access:

* Director: any class in their school
* Teacher: assigned classes only

---

### 6.4 Update Class

Endpoint:

```txt
PATCH /api/v1/classes/{id}/
```

Access:

* Director only

---

### 6.5 Delete Class

Endpoint:

```txt
DELETE /api/v1/classes/{id}/
```

Access:

* Director only

Important:

Do not delete a class if it already has important historical data unless soft delete is used.

---

## 7. Subject API

### 7.1 List Subjects

Endpoint:

```txt
GET /api/v1/subjects/
```

Access:

* Director
* Teacher

---

### 7.2 Create Subject

Endpoint:

```txt
POST /api/v1/subjects/
```

Access:

* Director only

Request example:

```json
{
  "name": "Mathematics"
}
```

---

### 7.3 Update Subject

Endpoint:

```txt
PATCH /api/v1/subjects/{id}/
```

Access:

* Director only

---

### 7.4 Delete Subject

Endpoint:

```txt
DELETE /api/v1/subjects/{id}/
```

Access:

* Director only

---

## 8. Student API

### 8.1 List Students

Endpoint:

```txt
GET /api/v1/students/
```

Purpose:

List students based on user role.

Access:

* Director: all students in the school
* Teacher: students in assigned classes only
* Parent: own children only

Optional filters:

```txt
?classroom_id=1
?is_active=true
?search=ahmed
```

---

### 8.2 Create Student

Endpoint:

```txt
POST /api/v1/students/
```

Access:

* Director only

Request example:

```json
{
  "classroom_id": 1,
  "student_code": "STU-001",
  "first_name": "Ahmed",
  "last_name": "Alami",
  "date_of_birth": "2012-05-10",
  "gender": "male"
}
```

---

### 8.3 Get Student Details

Endpoint:

```txt
GET /api/v1/students/{id}/
```

Access:

* Director: any student in their school
* Teacher: students in assigned classes only
* Parent: own children only

Response should include basic information:

```json
{
  "id": 1,
  "student_code": "STU-001",
  "first_name": "Ahmed",
  "last_name": "Alami",
  "classroom": {
    "id": 1,
    "name": "2AC A"
  },
  "is_active": true
}
```

---

### 8.4 Update Student

Endpoint:

```txt
PATCH /api/v1/students/{id}/
```

Access:

* Director only

---

### 8.5 Deactivate Student

Endpoint:

```txt
PATCH /api/v1/students/{id}/deactivate/
```

Access:

* Director only

---

## 9. Parent Student Relation API

### 9.1 Link Parent to Student

Endpoint:

```txt
POST /api/v1/parent-student-relations/
```

Access:

* Director only

Request example:

```json
{
  "parent_id": 1,
  "student_id": 1,
  "relationship": "father"
}
```

---

### 9.2 List Relations

Endpoint:

```txt
GET /api/v1/parent-student-relations/
```

Access:

* Director only

---

### 9.3 Remove Relation

Endpoint:

```txt
DELETE /api/v1/parent-student-relations/{id}/
```

Access:

* Director only

---

## 10. Teacher Class Assignment API

### 10.1 Assign Teacher to Class and Subject

Endpoint:

```txt
POST /api/v1/teacher-class-assignments/
```

Access:

* Director only

Request example:

```json
{
  "teacher_id": 1,
  "classroom_id": 1,
  "subject_id": 1
}
```

---

### 10.2 List Assignments

Endpoint:

```txt
GET /api/v1/teacher-class-assignments/
```

Access:

* Director: all assignments
* Teacher: own assignments only

---

### 10.3 Remove Assignment

Endpoint:

```txt
DELETE /api/v1/teacher-class-assignments/{id}/
```

Access:

* Director only

---

## 11. Timetable Session API

### 11.1 List Timetable Sessions

Endpoint:

```txt
GET /api/v1/timetable-sessions/
```

Access:

* Director: all sessions
* Teacher: assigned sessions only
* Parent: sessions related to their children only, through student timetable view

Optional filters:

```txt
?classroom_id=1
?teacher_id=1
?day_of_week=monday
```

---

### 11.2 Create Timetable Session

Endpoint:

```txt
POST /api/v1/timetable-sessions/
```

Access:

* Director only

Request example:

```json
{
  "classroom_id": 1,
  "teacher_id": 1,
  "subject_id": 1,
  "day_of_week": "monday",
  "start_time": "08:00",
  "end_time": "10:00"
}
```

---

### 11.3 Get Timetable Session Details

Endpoint:

```txt
GET /api/v1/timetable-sessions/{id}/
```

Access:

* Director
* Assigned teacher

---

### 11.4 Update Timetable Session

Endpoint:

```txt
PATCH /api/v1/timetable-sessions/{id}/
```

Access:

* Director only

---

### 11.5 Delete Timetable Session

Endpoint:

```txt
DELETE /api/v1/timetable-sessions/{id}/
```

Access:

* Director only

---

## 12. Attendance API

### 12.1 List Attendance Records

Endpoint:

```txt
GET /api/v1/attendance/
```

Access:

* Director: all attendance records in school
* Teacher: records related to assigned sessions/classes
* Parent: records for own children only

Optional filters:

```txt
?date=2026-06-08
?student_id=1
?classroom_id=1
?timetable_session_id=1
?status=absent
```

---

### 12.2 Mark Attendance

Endpoint:

```txt
POST /api/v1/attendance/mark/
```

Purpose:

Teacher marks attendance for one session.

Access:

* Assigned teacher only
* Director may also be allowed for correction/admin control

Request example:

```json
{
  "timetable_session_id": 1,
  "date": "2026-06-08",
  "records": [
    {
      "student_id": 1,
      "status": "present"
    },
    {
      "student_id": 2,
      "status": "absent"
    },
    {
      "student_id": 3,
      "status": "late"
    }
  ]
}
```

Response example:

```json
{
  "message": "Attendance saved successfully",
  "timetable_session_id": 1,
  "date": "2026-06-08",
  "total_records": 3
}
```

Important rule:

For each student, the system should create or update one attendance record for the same session and date.

---

### 12.3 Update Single Attendance Record

Endpoint:

```txt
PATCH /api/v1/attendance/{id}/
```

Access:

* Director
* Assigned teacher

---

### 12.4 Get Today Attendance Summary

Endpoint:

```txt
GET /api/v1/attendance/today-summary/
```

Purpose:

Show today’s attendance summary for the dashboard.

Access:

* Director only

Response example:

```json
{
  "date": "2026-06-08",
  "present": 120,
  "absent": 15,
  "late": 8,
  "excused": 2,
  "not_marked_sessions": 4
}
```

---

### 12.5 Get Student Attendance Calendar

Endpoint:

```txt
GET /api/v1/students/{id}/attendance-calendar/
```

Purpose:

Show attendance history for one student.

Access:

* Director
* Assigned teacher
* Parent of the student

Optional filters:

```txt
?month=6&year=2026
```

---

### 12.6 Get Student Current Status

Endpoint:

```txt
GET /api/v1/students/{id}/current-status/
```

Purpose:

Show if the student is currently present, absent, late, no class scheduled, or attendance not marked yet.

Access:

* Director
* Assigned teacher
* Parent of the student

Response example:

```json
{
  "student_id": 1,
  "current_status": "present_now",
  "session": {
    "id": 1,
    "subject": "Mathematics",
    "start_time": "08:00",
    "end_time": "10:00"
  }
}
```

---

## 13. Teacher Note API

### 13.1 List Teacher Notes

Endpoint:

```txt
GET /api/v1/teacher-notes/
```

Access:

* Director: all notes in school
* Teacher: notes created by them or for assigned students
* Parent: not included in MVP unless later decided

Optional filters:

```txt
?student_id=1
?teacher_id=1
?note_type=homework
```

---

### 13.2 Create Teacher Note

Endpoint:

```txt
POST /api/v1/teacher-notes/
```

Access:

* Teacher for assigned students
* Director

Request example:

```json
{
  "student_id": 1,
  "classroom_id": 1,
  "note_type": "homework",
  "title": "Homework missing",
  "content": "Ahmed did not bring homework today."
}
```

---

### 13.3 Get Teacher Note Details

Endpoint:

```txt
GET /api/v1/teacher-notes/{id}/
```

Access:

* Director
* Teacher who created the note

---

### 13.4 Update Teacher Note

Endpoint:

```txt
PATCH /api/v1/teacher-notes/{id}/
```

Access:

* Teacher who created the note
* Director

---

### 13.5 Delete Teacher Note

Endpoint:

```txt
DELETE /api/v1/teacher-notes/{id}/
```

Access:

* Director
* Teacher who created the note

---

## 14. Student Payment API

### 14.1 List Payments

Endpoint:

```txt
GET /api/v1/payments/
```

Access:

* Director only

Optional filters:

```txt
?student_id=1
?month=6
?year=2026
?status=unpaid
```

---

### 14.2 Create Payment Record

Endpoint:

```txt
POST /api/v1/payments/
```

Access:

* Director only

Request example:

```json
{
  "student_id": 1,
  "month": 6,
  "year": 2026,
  "amount_due": "800.00",
  "amount_paid": "0.00",
  "status": "unpaid",
  "due_date": "2026-06-10"
}
```

---

### 14.3 Update Payment Record

Endpoint:

```txt
PATCH /api/v1/payments/{id}/
```

Access:

* Director only

Request example:

```json
{
  "amount_paid": "800.00",
  "status": "paid"
}
```

---

### 14.4 Payment Summary

Endpoint:

```txt
GET /api/v1/payments/summary/
```

Access:

* Director only

Response example:

```json
{
  "month": 6,
  "year": 2026,
  "paid_students": 80,
  "unpaid_students": 20,
  "partial_students": 5,
  "late_students": 10,
  "total_amount_due": "80000.00",
  "total_amount_paid": "62000.00"
}
```

---

## 15. Director Dashboard API

### 15.1 Dashboard Summary

Endpoint:

```txt
GET /api/v1/dashboard/director/
```

Access:

* Director only

Purpose:

Show main school statistics.

Response example:

```json
{
  "total_students": 250,
  "today_attendance": {
    "present": 200,
    "absent": 30,
    "late": 10,
    "excused": 5,
    "not_marked_sessions": 3
  },
  "payments": {
    "paid_students": 180,
    "unpaid_students": 40,
    "partial_students": 20,
    "late_students": 10
  },
  "latest_teacher_notes": [
    {
      "id": 1,
      "student_name": "Ahmed Alami",
      "teacher_name": "Mr. Yassine",
      "note_type": "homework",
      "title": "Homework missing",
      "created_at": "2026-06-08T10:30:00Z"
    }
  ],
  "class_overview": [
    {
      "classroom_id": 1,
      "classroom_name": "2AC A",
      "total_students": 30,
      "attendance_marked_today": true
    }
  ]
}
```

---

## 16. Parent Dashboard API

### 16.1 Parent Children

Endpoint:

```txt
GET /api/v1/parent/children/
```

Access:

* Parent only

Purpose:

Return children linked to the parent.

Response example:

```json
[
  {
    "id": 1,
    "full_name": "Ahmed Alami",
    "classroom": "2AC A"
  },
  {
    "id": 2,
    "full_name": "Sara Alami",
    "classroom": "1AC B"
  }
]
```

---

### 16.2 Child Today Attendance

Endpoint:

```txt
GET /api/v1/parent/children/{student_id}/today-attendance/
```

Access:

* Parent of the student only

Response example:

```json
{
  "student_id": 1,
  "date": "2026-06-08",
  "sessions": [
    {
      "time": "08:00-10:00",
      "subject": "Mathematics",
      "status": "present"
    },
    {
      "time": "10:00-12:00",
      "subject": "Arabic",
      "status": "not_marked"
    }
  ]
}
```

---

### 16.3 Child Attendance Calendar

Endpoint:

```txt
GET /api/v1/parent/children/{student_id}/attendance-calendar/
```

Access:

* Parent of the student only

Optional filters:

```txt
?month=6&year=2026
```

---

### 16.4 Child Current Status

Endpoint:

```txt
GET /api/v1/parent/children/{student_id}/current-status/
```

Access:

* Parent of the student only

Purpose:

Return the current session status of the child.

---

## 17. Teacher Dashboard API

### 17.1 Teacher Dashboard

Endpoint:

```txt
GET /api/v1/dashboard/teacher/
```

Access:

* Teacher only

Purpose:

Show teacher’s assigned sessions and classes.

Response example:

```json
{
  "today_sessions": [
    {
      "id": 1,
      "classroom": "2AC A",
      "subject": "Mathematics",
      "start_time": "08:00",
      "end_time": "10:00",
      "attendance_marked": true
    }
  ],
  "assigned_classes": [
    {
      "id": 1,
      "name": "2AC A"
    }
  ]
}
```

---

## 18. API Permission Summary

| API Area                  | Director  | Teacher           | Parent             |
| ------------------------- | --------- | ----------------- | ------------------ |
| Authentication            | Yes       | Yes               | Yes                |
| School Info               | View/Edit | View              | View               |
| Users                     | Full      | No                | No                 |
| Classes                   | Full      | Assigned only     | No direct access   |
| Subjects                  | Full      | View              | No                 |
| Students                  | Full      | Assigned only     | Own children only  |
| Parent-Student Relations  | Full      | No                | No                 |
| Teacher-Class Assignments | Full      | Own only          | No                 |
| Timetable Sessions        | Full      | Assigned only     | Child-related only |
| Attendance                | Full      | Assigned only     | Own children only  |
| Teacher Notes             | Full      | Own/assigned only | No for MVP         |
| Payments                  | Full      | No                | No for MVP         |
| Director Dashboard        | Yes       | No                | No                 |
| Teacher Dashboard         | No        | Yes               | No                 |
| Parent Dashboard          | No        | No                | Yes                |

---

## 19. MVP API Build Priority

The backend APIs should be built in this order:

1. Authentication API
2. School API
3. User Management API
4. ClassRoom API
5. Subject API
6. Student API
7. ParentStudentRelation API
8. TeacherClassAssignment API
9. TimetableSession API
10. Attendance API
11. TeacherNote API
12. StudentPayment API
13. Director Dashboard API
14. Teacher Dashboard API
15. Parent Dashboard API

This order follows the entity dependencies and user journey.

---

## 20. API Development Rules for Codex

When Codex starts implementing the API, it should follow these rules:

* Build one API area at a time.
* Do not build all endpoints at once.
* Start with models, serializers, permissions, then views.
* Keep the MVP simple.
* Respect role-based access.
* Respect school-based data isolation.
* Do not expose data from another school.
* Do not allow parents to access students not linked to them.
* Do not allow teachers to access classes not assigned to them.
* Use clear endpoint names.
* Return JSON responses.
* Add filters only where useful for the MVP.
* Avoid advanced features unless requested later.

---

## 21. Final Summary

The API should support the main MVP flow:

```txt
Director creates school data → Teacher marks attendance → Parent sees child status → Director sees dashboard visibility
```

The most important APIs are:

1. Authentication
2. Students
3. Classes
4. Timetable Sessions
5. Attendance
6. Parent Dashboard
7. Director Dashboard

The API should be simple, clean, and ready for future frontend and Flutter mobile app integration.
