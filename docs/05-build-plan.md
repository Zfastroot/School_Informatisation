# Build Plan Document — School Management Platform MVP

## 1. Purpose

This document defines the step-by-step build plan for the School Management Platform MVP.

The goal is to help development stay organized, simple, and controlled.

This document is especially important when working with Codex, because Codex should build the project one small step at a time instead of generating the whole platform at once.

Related documents:

* `docs/01-mvp-scope.md`
* `docs/02-user-journey.md`
* `docs/03-entities-relationships.md`
* `docs/04-api-plan.md`

---

## 2. Development Strategy

The MVP should be built in small phases.

Each phase should have:

* A clear goal
* A small set of files to change
* A simple way to test the result
* A clear stopping point

Codex should not move to the next phase until the current phase is reviewed.

The project should follow an API-first approach.

This means the backend should be built cleanly so it can support:

* Web dashboard first
* Flutter mobile app later
* Parent and teacher mobile interfaces later

---

## 3. Recommended Tech Stack

### 3.1 Backend

The backend should use:

* Python
* Django
* Django REST Framework
* SQLite for local MVP development
* JWT authentication if authentication is implemented
* Django admin for internal testing and data management

### 3.2 Frontend

The frontend is not the first priority.

The MVP can start with:

* Django admin
* API testing using Postman, Insomnia, or browser-based API views
* A simple web dashboard later

### 3.3 Future Mobile App

A Flutter mobile app can be added later after the backend API is stable.

---

## 4. Repository Structure

The recommended project structure is:

```txt
school-informatization/
│
├── AGENTS.md
├── README.md
├── .gitignore
│
├── docs/
│   ├── 01-mvp-scope.md
│   ├── 02-user-journey.md
│   ├── 03-entities-relationships.md
│   ├── 04-api-plan.md
│   ├── 05-build-plan.md
│   └── assets/
│       └── mermaid-diagram.png
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── apps/
│       ├── accounts/
│       ├── schools/
│       ├── academics/
│       ├── attendance/
│       ├── notes/
│       ├── payments/
│       ├── dashboard/
│       └── common/
│
└── frontend/
    ├── package.json
    ├── README.md
    ├── .env.example
    ├── public/
    └── src/
        ├── app/
        ├── components/
        ├── features/
        │   ├── auth/
        │   ├── director/
        │   ├── teacher/
        │   ├── parent/
        │   ├── students/
        │   ├── classes/
        │   ├── attendance/
        │   ├── notes/
        │   └── payments/
        ├── services/
        │   └── api/
        ├── hooks/
        ├── utils/
        └── styles/
```

For the first development phases, the `frontend/` folder can exist but stay empty until the backend APIs are ready.

However, the final MVP must include both:

```txt
Backend API + Web Frontend
```

Django admin and API tools are only for development and testing. They are not the final MVP interface.


---

## 5. Backend Apps Plan

To keep the backend organized, the MVP can use these Django apps:

| App        | Responsibility                                                                               |
| ---------- | -------------------------------------------------------------------------------------------- |
| accounts   | User, roles, DirectorProfile, TeacherProfile, ParentProfile, authentication                  |
| schools    | School model and school-level settings                                                       |
| academics  | ClassRoom, Subject, Student, TeacherClassAssignment, ParentStudentRelation, TimetableSession |
| attendance | AttendanceRecord and attendance marking logic                                                |
| notes      | TeacherNote                                                                                  |
| payments   | StudentPayment                                                                               |
| dashboard  | Director, Teacher, and Parent dashboard APIs                                                 |
| common     | Shared permissions, utilities, constants, validators                                         |

Alternative:

If the project becomes too complicated, some apps can be merged during the MVP.

The important rule is to keep the code understandable and not over-engineered.

---

## 6. Build Phases

## Phase 0 — Documentation Setup

### Goal

Prepare the project documentation so Codex understands the MVP.

### Tasks

1. Create the `docs/` folder.
2. Add all planning documents.
3. Add the ERD image inside `docs/assets/`.
4. Create `AGENTS.md`.
5. Create `README.md`.

### Expected Files

```txt
AGENTS.md
README.md
docs/01-mvp-scope.md
docs/02-user-journey.md
docs/03-entities-relationships.md
docs/04-api-plan.md
docs/05-build-plan.md
docs/assets/mermaid-diagram.png
```

### Test

Ask Codex to read the documents and summarize:

* The MVP idea
* The users
* The entities
* The build order

### Stop Point

Stop after Codex correctly understands the project.

---

## Phase 1 — Backend Project Initialization

### Goal

Create the initial Django backend project.

### Tasks

1. Create the `backend/` folder.
2. Create a Python virtual environment.
3. Install Django and Django REST Framework.
4. Create the Django project.
5. Create `requirements.txt`.
6. Configure basic settings.
7. Run the first migration.
8. Confirm the server starts.

### Expected Files

```txt
backend/manage.py
backend/config/settings.py
backend/config/urls.py
backend/requirements.txt
```

### Test

Run:

```bash
python manage.py runserver
```

Expected result:

The Django server should start without errors.

### Stop Point

Stop after the backend project runs successfully.

---

## Phase 2 — Create Django Apps

### Goal

Create the main Django apps for the MVP.

### Tasks

Create these apps:

```txt
accounts
schools
academics
attendance
notes
payments
dashboard
common
```

Register the apps in Django settings.

### Expected Apps

```txt
backend/apps/accounts/
backend/apps/schools/
backend/apps/academics/
backend/apps/attendance/
backend/apps/notes/
backend/apps/payments/
backend/apps/dashboard/
backend/apps/common/
```

### Test

Run:

```bash
python manage.py check
```

Expected result:

No Django configuration errors.

### Stop Point

Stop after all apps are created and registered.

---

## Phase 3 — Core Models

### Goal

Create the database models from the entity relationship document.

### Tasks

Create models for:

1. School
2. User
3. DirectorProfile
4. TeacherProfile
5. ParentProfile
6. ClassRoom
7. Subject
8. Student
9. ParentStudentRelation
10. TeacherClassAssignment
11. TimetableSession
12. AttendanceRecord
13. TeacherNote
14. StudentPayment

### Important Rules

* Use `school` foreign key on school-owned entities.
* Use role choices for users.
* Use status choices for attendance and payments.
* Add unique constraints:

  * Student + TimetableSession + Date
  * Student + Month + Year
  * Teacher + ClassRoom + Subject
  * Parent + Student
* Keep fields simple for MVP.
* Do not add features not listed in the documents.

### Test

Run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py check
```

Expected result:

Migrations are created and applied successfully.

### Stop Point

Stop after all models migrate correctly.

---

## Phase 4 — Django Admin Setup

### Goal

Register MVP models in Django admin for quick testing.

### Tasks

1. Register all models in admin.
2. Add useful list displays.
3. Add filters for school, class, status, date where useful.
4. Create a superuser.

### Test

Run:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Then open:

```txt
/admin/
```

Expected result:

Admin can log in and manage MVP data.

### Stop Point

Stop after models are visible in Django admin.

---

## Phase 5 — Serializers

### Goal

Create DRF serializers for all MVP models.

### Tasks

Create serializers for:

* School
* User
* DirectorProfile
* TeacherProfile
* ParentProfile
* ClassRoom
* Subject
* Student
* ParentStudentRelation
* TeacherClassAssignment
* TimetableSession
* AttendanceRecord
* TeacherNote
* StudentPayment

### Rules

* Keep serializers simple.
* Do not over-nest everything.
* Use IDs for write operations.
* Use small nested objects only for readable responses when useful.

### Test

Run:

```bash
python manage.py check
```

Expected result:

No serializer import or configuration errors.

### Stop Point

Stop after serializers are created.

---

## Phase 6 — Permissions

### Goal

Create role-based and school-based permissions.

### Tasks

Create permission logic for:

* Director access
* Teacher access
* Parent access
* School data isolation
* Parent-child access
* Teacher-assigned-class access

### Main Rules

Director:

* Can access all data inside their school.

Teacher:

* Can access assigned classes, sessions, students, attendance, and notes only.

Parent:

* Can access only their linked children and child attendance.

### Test

Test manually using different user roles.

Expected result:

Users cannot access data outside their role or school.

### Stop Point

Stop after basic permission logic exists.

---

## Phase 7 — Authentication API

### Goal

Allow users to log in and access protected endpoints.

### Tasks

1. Configure JWT authentication.
2. Create login endpoint.
3. Create refresh token endpoint.
4. Create current user endpoint `/api/v1/auth/me/`.

### Endpoints

```txt
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
GET /api/v1/auth/me/
```

### Test

Use Postman or browser API:

1. Log in.
2. Copy access token.
3. Call `/api/v1/auth/me/`.

Expected result:

The logged-in user data and role are returned correctly.

### Stop Point

Stop after authentication works.

---

## Phase 8 — Basic CRUD APIs

### Goal

Create the basic CRUD endpoints for core school data.

### APIs to Build

1. School API
2. User Management API
3. ClassRoom API
4. Subject API
5. Student API
6. ParentStudentRelation API
7. TeacherClassAssignment API
8. TimetableSession API

### Rules

* Build one API area at a time.
* Use DRF ViewSets where useful.
* Apply permissions from Phase 6.
* Add simple filters where useful.
* Do not build dashboard logic yet.

### Test

Use API endpoints to:

1. Create a school.
2. Create users.
3. Create classes.
4. Create subjects.
5. Create students.
6. Link parents to students.
7. Assign teachers to classes.
8. Create timetable sessions.

### Stop Point

Stop after the main school setup flow works.

---

## Phase 9 — Attendance API

### Goal

Allow teachers to mark attendance by session.

### Tasks

1. Create attendance list endpoint.
2. Create attendance marking endpoint.
3. Allow create/update attendance records for a session and date.
4. Add attendance filters.
5. Add student attendance calendar endpoint.
6. Add student current status endpoint.

### Important Logic

When a teacher marks attendance:

* The teacher must be assigned to the session.
* The session must belong to the teacher’s school.
* Each student must belong to the session classroom.
* The system should create or update one record per student/session/date.

### Endpoints

```txt
GET /api/v1/attendance/
POST /api/v1/attendance/mark/
PATCH /api/v1/attendance/{id}/
GET /api/v1/students/{id}/attendance-calendar/
GET /api/v1/students/{id}/current-status/
```

### Test

1. Create class.
2. Create students.
3. Create teacher.
4. Assign teacher to class and subject.
5. Create session.
6. Log in as teacher.
7. Mark attendance.
8. Log in as parent.
9. Confirm parent can see child attendance.

### Stop Point

Stop after the full attendance flow works.

---

## Phase 10 — Teacher Notes API

### Goal

Allow teachers to write notes about students.

### Tasks

1. Create teacher notes endpoints.
2. Allow teacher to add notes for assigned students.
3. Allow director to view all notes.
4. Prevent teachers from writing notes for unrelated students.

### Endpoints

```txt
GET /api/v1/teacher-notes/
POST /api/v1/teacher-notes/
GET /api/v1/teacher-notes/{id}/
PATCH /api/v1/teacher-notes/{id}/
DELETE /api/v1/teacher-notes/{id}/
```

### Test

1. Log in as teacher.
2. Create note for assigned student.
3. Try to create note for unrelated student.
4. Confirm unrelated student is rejected.
5. Log in as director.
6. Confirm director can view all notes.

### Stop Point

Stop after teacher notes work correctly.

---

## Phase 11 — Student Payment API

### Goal

Allow the director to manually track student payments.

### Tasks

1. Create payment CRUD endpoints.
2. Add monthly payment uniqueness.
3. Add payment filters.
4. Add payment summary endpoint.

### Endpoints

```txt
GET /api/v1/payments/
POST /api/v1/payments/
PATCH /api/v1/payments/{id}/
GET /api/v1/payments/summary/
```

### Test

1. Log in as director.
2. Create payment records.
3. Update payment status.
4. Filter unpaid students.
5. View payment summary.

### Stop Point

Stop after payment tracking works.

---

## Phase 12 — Dashboard APIs

### Goal

Create simple dashboards for each role.

### APIs to Build

Director:

```txt
GET /api/v1/dashboard/director/
```

Teacher:

```txt
GET /api/v1/dashboard/teacher/
```

Parent:

```txt
GET /api/v1/parent/children/
GET /api/v1/parent/children/{student_id}/today-attendance/
GET /api/v1/parent/children/{student_id}/attendance-calendar/
GET /api/v1/parent/children/{student_id}/current-status/
```

### Rules

The dashboard should return summarized data only.

Do not make the dashboard too complex in the MVP.

### Test

1. Director sees school overview.
2. Teacher sees today’s assigned sessions.
3. Parent sees children and attendance status.

### Stop Point

Stop after role dashboards return correct data.

---

## Phase 13 — Frontend MVP

### Goal

Build a simple web frontend to test and demonstrate the MVP.

The frontend is part of the MVP.

Django admin and API tools are useful for development, but the final MVP should have real user screens for Director, Teacher, and Parent.

### Frontend Screens

The first frontend MVP should include:

#### Authentication

* Login page
* Logout flow
* Role-based redirect after login

#### Director Screens

* Director dashboard
* Students list
* Create/edit student
* Classes list
* Create/edit class
* Teachers list
* Create/edit teacher
* Parents list
* Create/edit parent
* Parent-student linking
* Teacher-class-subject assignment
* Timetable sessions
* Attendance overview
* Teacher notes overview
* Payment tracking

#### Teacher Screens

* Teacher dashboard
* Assigned sessions
* Session student list
* Mark attendance screen
* Add teacher note screen
* View previous notes for assigned students

#### Parent Screens

* Parent dashboard
* Children list
* Child current status
* Today attendance by session
* Attendance calendar/history

### Frontend Rules

* Keep the design simple.
* Focus on usability, not perfect UI.
* Use the backend APIs from `docs/04-api-plan.md`.
* Respect role-based access.
* Do not add features outside the MVP.
* Build screens one by one.
* Start with the most important flow.

### Most Important Frontend Flow

The first frontend flow to build should be:

```txt
Teacher logs in → selects session → marks attendance → parent logs in → sees child status → director sees dashboard update
```

This is the core MVP value.

### Test

The MVP frontend is working when:

1. Director can log in and set up school data.
2. Teacher can log in and mark attendance.
3. Parent can log in and view child attendance.
4. Director can see dashboard visibility.

### Stop Point

Stop after the main MVP flow works from the frontend.

---

## Phase 14 — Testing and Cleanup

### Goal

Make sure the MVP is stable enough for a pilot test.

### Tasks

1. Test all core flows.
2. Fix permission bugs.
3. Fix school isolation bugs.
4. Clean unused code.
5. Improve README.
6. Add example test data.
7. Prepare a demo script.

### Core Flows to Test

1. Director creates school setup.
2. Director creates teacher, parent, and student.
3. Director creates class, subject, and session.
4. Director links parent to student.
5. Teacher marks attendance.
6. Parent sees child status.
7. Teacher adds note.
8. Director sees dashboard.
9. Director updates payment status.

### Stop Point

Stop after the MVP is ready for pilot testing.

---

## 7. Codex Working Rules

When using Codex, use this pattern for every development task:

```txt
Read AGENTS.md and the docs related to this task.

Task:
Do only [specific small task].

Rules:
- Do not add features outside the docs.
- Do not modify unrelated files.
- Keep the MVP simple.
- Respect school-based data isolation.
- Respect role-based permissions.
- Stop after completing this task.

Output:
Tell me:
1. What files changed
2. What was added
3. How to test it
4. What the next step should be
```

---

## 8. Good Codex Prompts by Phase

### Prompt for Phase 0

```txt
Read AGENTS.md and all documents inside docs/.
Do not write code yet.

Summarize:
1. The MVP idea
2. The users and roles
3. The main entities
4. The main flows
5. The backend build order

If something is unclear, ask questions.
```

---

### Prompt for Phase 1

```txt
Read AGENTS.md and docs/05-build-plan.md.

Create only the initial Django backend project inside /backend.
Install Django and Django REST Framework.
Create requirements.txt.
Do not create business models yet.

After finishing, tell me:
1. What files changed
2. How to run the server
3. What the next step is
```

---

### Prompt for Phase 2

```txt
Read AGENTS.md and docs/05-build-plan.md.

Create the Django apps listed in Phase 2.
Register them in settings.
Do not create models yet.

After finishing, run or explain how to run:
python manage.py check
```

---

### Prompt for Phase 3

```txt
Read docs/03-entities-relationships.md and docs/05-build-plan.md.

Create only the MVP database models.
Respect the fields, relationships, choices, and unique constraints.
Do not create APIs yet.

After finishing, tell me:
1. What models were created
2. What migrations to run
3. What the next step is
```

---

### Prompt for Phase 4

```txt
Read docs/03-entities-relationships.md and docs/05-build-plan.md.

Register all MVP models in Django admin.
Add simple list_display and filters where useful.
Do not create APIs yet.

After finishing, tell me how to test in Django admin.
```

---

### Prompt for Phase 5

```txt
Read docs/04-api-plan.md and docs/05-build-plan.md.

Create serializers for all MVP models.
Keep them simple.
Use IDs for write operations.
Do not create views yet.

After finishing, summarize the serializers created.
```

---

### Prompt for Phase 6

```txt
Read docs/02-user-journey.md, docs/03-entities-relationships.md, and docs/04-api-plan.md.

Create permission classes for Director, Teacher, Parent, school isolation, parent-child access, and teacher-assigned access.
Do not create full API views yet.

After finishing, explain how each permission works.
```

---

### Prompt for Phase 7

```txt
Read docs/04-api-plan.md and docs/05-build-plan.md.

Implement authentication endpoints:
- POST /api/v1/auth/login/
- POST /api/v1/auth/refresh/
- GET /api/v1/auth/me/

Use JWT.
Do not create business CRUD APIs yet.

After finishing, explain how to test login and me endpoint.
```

---

### Prompt for Phase 8

```txt
Read docs/04-api-plan.md and docs/05-build-plan.md.

Implement only the basic CRUD APIs for:
- School
- User
- ClassRoom
- Subject
- Student
- ParentStudentRelation
- TeacherClassAssignment
- TimetableSession

Apply role-based permissions and school isolation.
Do not implement attendance, notes, payments, or dashboards yet.

After finishing, list the endpoints created and how to test them.
```

---

### Prompt for Phase 9

```txt
Read docs/04-api-plan.md and docs/05-build-plan.md.

Implement the Attendance API only:
- GET /api/v1/attendance/
- POST /api/v1/attendance/mark/
- PATCH /api/v1/attendance/{id}/
- GET /api/v1/students/{id}/attendance-calendar/
- GET /api/v1/students/{id}/current-status/

Respect teacher assignment, parent-child access, and school isolation.

After finishing, explain how to test the full attendance flow.
```

---

### Prompt for Phase 10

```txt
Read docs/04-api-plan.md and docs/05-build-plan.md.

Implement Teacher Notes API only.
Respect teacher-assigned-student access and director access.
Do not implement payments or dashboards yet.

After finishing, explain how to test notes.
```

---

### Prompt for Phase 11

```txt
Read docs/04-api-plan.md and docs/05-build-plan.md.

Implement Student Payment API only.
Director-only access.
Include payment summary endpoint.
Do not implement dashboards yet.

After finishing, explain how to test payment tracking.
```

---

### Prompt for Phase 12

```txt
Read docs/04-api-plan.md and docs/05-build-plan.md.

Implement dashboard APIs:
- Director dashboard
- Teacher dashboard
- Parent dashboard endpoints

Keep the dashboard simple and MVP-focused.

After finishing, explain how to test each dashboard.
```

---

## 9. Git Workflow

Use small commits.

Recommended branches:

```txt
main
dev
feature/docs-setup
feature/backend-init
feature/models
feature/auth
feature/crud-apis
feature/attendance
feature/dashboard
```

Simple workflow:

1. Work on `dev`.
2. Create feature branches for bigger work.
3. Merge only when the phase works.
4. Keep `main` stable.

Example commit messages:

```txt
docs: add MVP planning documents
backend: initialize Django project
backend: create MVP models
backend: register models in admin
api: add authentication endpoints
api: add student CRUD endpoints
api: add attendance marking endpoint
api: add director dashboard endpoint
```

---

## 10. MVP Completion Criteria

The MVP is considered complete when:

* Director can log in.
* Director can create classes, subjects, teachers, parents, and students.
* Director can link parents to students.
* Director can assign teachers to classes and subjects.
* Director can create timetable sessions.
* Teacher can log in.
* Teacher can view assigned sessions.
* Teacher can mark attendance by session.
* Parent can log in.
* Parent can view children.
* Parent can view today’s attendance.
* Parent can view attendance calendar.
* Teacher can create notes.
* Director can view notes.
* Director can track payments manually.
* Director can view dashboard summary.

---

## 11. Final Summary

The build plan should follow this order:

```txt
Docs → Backend Init → Apps → Models → Admin → Serializers → Permissions → Auth → CRUD APIs → Attendance → Notes → Payments → Dashboards → Frontend MVP → Demo
```

The first goal is not to build a complete school ERP.

The first goal is to build a clean and usable MVP that proves the value:

```txt
Teacher marks attendance → Parent sees child status → Director sees school visibility
```

The MVP must include both:

```txt
Backend API + Web Frontend
```

Django admin and API testing tools are only for development and internal testing.

They are not the final MVP interface.
