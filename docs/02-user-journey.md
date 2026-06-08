# User Journey Document — School Management Platform MVP

## 1. Purpose

This document explains how each user will use the MVP.

The main users are:

* Director / Admin
* Teacher / Professor
* Parent

The goal is to make the app flow clear before starting development.

This document should help define the screens, backend logic, permissions, and API endpoints later.

---

## 2. Director / Admin Journey

### 2.1 Main Goal

The director wants to control the school from one place and see what is happening every day.

The director is the main decision-maker and has the highest access level in the MVP.

---

### 2.2 Step 1: Login

The director logs in using email or phone number and password.

After login, the director goes to the main dashboard.

---

### 2.3 Step 2: View Dashboard

The director sees a daily overview of the school.

The dashboard should show:

* Total students
* Today’s present students
* Today’s absent students
* Late students
* Attendance not marked yet
* Unpaid students
* Latest teacher notes
* Class overview

The dashboard is important because it gives the director fast visibility without asking teachers or checking notebooks manually.

---

### 2.4 Step 3: Manage Classes

The director creates and manages classes.

Examples:

* 1AC A
* 2AC B
* 3AC A

The director can:

* Create classes
* Edit classes
* Delete classes
* View students inside each class

---

### 2.5 Step 4: Manage Teachers

The director creates teacher accounts.

Each teacher can be assigned to one or more classes and subjects.

Example:

* Teacher: Mr. Yassine
* Subject: Mathematics
* Class: 2AC A

The director can:

* Add teachers
* Edit teacher information
* Assign teachers to classes
* Assign teachers to subjects
* Deactivate teacher accounts if needed

---

### 2.6 Step 5: Manage Students

The director adds students and connects them to a class.

Each student has:

* Full name
* Class
* Parent account
* Payment status
* Attendance history
* Teacher notes

The director can:

* Create students
* Edit student information
* Move a student to another class
* Link a student to one or more parents/guardians
* View the student profile

---

### 2.7 Step 6: Manage Parents

The director creates parent accounts and connects each parent to one or more children.

Example:

* Parent: Mohamed Alami
* Children: Ahmed Alami, Sara Alami

The director can:

* Create parent accounts
* Edit parent information
* Link parents to students
* View children linked to each parent

---

### 2.8 Step 7: Create Timetable Sessions

The director creates class sessions by day and time.

Examples:

* Monday 08:00–10:00 — Mathematics — 2AC A
* Monday 10:00–12:00 — Arabic — 2AC A

Each session should include:

* Class
* Subject
* Teacher
* Day
* Start time
* End time

This allows attendance to be tracked by session, not only by day.

---

### 2.9 Step 8: Monitor Attendance

The director can view attendance by:

* Date
* Class
* Student
* Teacher
* Session

The director can see:

* Which students are present
* Which students are absent
* Which students are late
* Which students are excused
* Which sessions are not marked yet

This helps the director know what is happening in the school during the day.

---

### 2.10 Step 9: Monitor Payments

The director tracks student payments manually.

Payment status can be:

* Paid
* Unpaid
* Partial
* Late

The director can:

* View payment status by student
* Update payment status manually
* See unpaid students
* See monthly payment summaries

Online payment is not part of the MVP.

---

### 2.11 Step 10: Read Teacher Notes

The director can view notes written by teachers about students.

Examples:

* Behavior note
* Homework note
* Performance note
* Discipline note
* General note

The director can view notes from:

* Student profile
* Teacher notes section
* Director dashboard

---

## 3. Teacher Journey

### 3.1 Main Goal

The teacher wants to manage daily class attendance and write notes about students.

The teacher should only see the classes, sessions, and students assigned to them.

---

### 3.2 Step 1: Login

The teacher logs in using email or phone number and password.

After login, the teacher goes to the teacher dashboard.

---

### 3.3 Step 2: View Assigned Classes and Sessions

The teacher sees only the classes and sessions assigned to them.

Examples:

* Monday 08:00–10:00 — Mathematics — 2AC A
* Tuesday 10:00–12:00 — Mathematics — 3AC B

The teacher should not see all school classes unless they are assigned to them.

---

### 3.4 Step 3: Select a Session

The teacher selects the current class session.

The system shows the list of students in that class.

The teacher can then start marking attendance for that session.

---

### 3.5 Step 4: Mark Attendance

The teacher marks each student as:

* Present
* Absent
* Late
* Excused

If the teacher has not marked attendance yet, the status should be considered:

* Not marked

After saving, the attendance becomes visible to:

* Director dashboard
* Parent dashboard

---

### 3.6 Step 5: Add Teacher Notes

The teacher can open a student profile and add a note.

Examples:

* “Ahmed did not bring homework.”
* “Sara participated well today.”
* “Youssef was late to class.”

A note should include:

* Student
* Teacher
* Note type
* Note content
* Date and time

---

### 3.7 Step 6: View Previous Notes

The teacher can view previous notes for students in assigned classes.

The teacher should not access students outside their assigned classes.

---

## 4. Parent Journey

### 4.1 Main Goal

The parent wants to know if their child is present, absent, late, or currently in class.

The parent should only see their own children.

---

### 4.2 Step 1: Login

The parent logs in using email or phone number and password.

After login, the parent goes to the parent dashboard.

---

### 4.3 Step 2: View Children List

The parent sees a list of their children.

Example:

* Ahmed Alami
* Sara Alami

The parent selects one child to view details.

---

### 4.4 Step 3: View Today’s Status

The parent sees the selected child’s current school status.

Examples:

* Present now
* Absent from current session
* Late
* No class scheduled now
* Attendance not marked yet

This is one of the most important parent features in the MVP.

---

### 4.5 Step 4: View Today’s Attendance

The parent sees today’s timetable and attendance status by session.

Example:

* 08:00–10:00 Mathematics — Present
* 10:00–12:00 Arabic — Absent
* 14:00–16:00 Physics — Not marked yet

This helps the parent understand the child’s attendance during the whole day.

---

### 4.6 Step 5: View Attendance Calendar

The parent can view attendance history by day, week, or month.

The calendar shows:

* Present
* Absent
* Late
* Excused
* No class
* Not marked

---

### 4.7 Step 6: View Basic Student Information

The parent can see basic information about the child:

* Name
* Class
* School
* Attendance summary

The parent should not be able to edit student information.

---

## 5. Student Journey

The student does not have an account in the MVP.

The student exists only as a profile managed by the school.

A student account may be added later after the MVP.

---

## 6. Main MVP Flows

### 6.1 Flow 1: Setup School Data

1. Director logs in.
2. Director creates classes.
3. Director creates teacher accounts.
4. Director creates parent accounts.
5. Director creates students.
6. Director links students to parents.
7. Director assigns teachers to classes and subjects.
8. Director creates timetable sessions.

---

### 6.2 Flow 2: Mark Attendance

1. Teacher logs in.
2. Teacher opens assigned session.
3. Teacher sees student list.
4. Teacher marks attendance.
5. Teacher saves attendance.
6. Director sees updated attendance.
7. Parent sees child attendance status.

---

### 6.3 Flow 3: Parent Checks Child Status

1. Parent logs in.
2. Parent selects child.
3. Parent sees current status.
4. Parent checks today’s attendance.
5. Parent checks calendar history.

---

### 6.4 Flow 4: Teacher Adds Note

1. Teacher logs in.
2. Teacher selects class or student.
3. Teacher writes note.
4. Note is saved.
5. Director can view the note.

---

### 6.5 Flow 5: Director Tracks Payments

1. Director logs in.
2. Director opens payment section.
3. Director selects student or month.
4. Director updates payment status.
5. Dashboard updates unpaid and paid summary.

---

## 7. Access Rules

### 7.1 Director / Admin Access

The director can access and manage:

* Classes
* Teachers
* Parents
* Students
* Sessions
* Attendance
* Payments
* Teacher notes
* Dashboard

The director has full access in the MVP.

---

### 7.2 Teacher Access

The teacher can access:

* Assigned classes
* Assigned sessions
* Students inside assigned classes
* Attendance marking for assigned sessions
* Notes for assigned students

The teacher cannot:

* Manage payments
* Manage parent accounts
* Manage school settings
* View unrelated classes
* View unrelated students

---

### 7.3 Parent Access

The parent can access:

* Their own children
* Today’s attendance for their children
* Attendance calendar for their children
* Basic student information for their children

The parent cannot:

* View other students
* Edit student data
* Mark attendance
* View school-wide dashboard
* View payments of other students
* View teacher/admin sections

---

## 8. MVP Journey Summary

The MVP journey is simple:

* Director sets up and monitors the school.
* Teacher marks attendance and adds notes.
* Parent follows child attendance from their own dashboard.
* Student does not log in during the MVP.

The most important journey is:

Teacher marks attendance → Parent sees child status → Director sees school visibility.

This flow is the core value of the MVP.
