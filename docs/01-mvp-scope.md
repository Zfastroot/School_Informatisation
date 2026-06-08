# MVP Scope Document — School Management Platform

## 1. Idea

The project is a web-based school management platform that connects the school administration, teachers, and parents in one place.

The platform helps schools manage students, classes, attendance, parent visibility, teacher notes, payment tracking, and the director dashboard from a single system.

The first version will be web-based, but the backend should be built in a clean API-first way so that mobile apps can be created later using Flutter.

---

## 2. Problem

Many private schools still manage daily operations using notebooks, Excel files, WhatsApp messages, and manual follow-up.

This creates problems such as:

* Attendance is difficult to track clearly.
* Parents do not always know if their child is present or absent.
* Directors do not have real-time visibility.
* Teachers write notes in different places.
* Payment tracking can become messy.
* WhatsApp communication is not organized.
* School data is scattered between notebooks, phones, and Excel files.

The main problem is that the school does not have one clear place to manage and monitor daily student activity.

---

## 3. Target Customer

The target customer is the school owner, director, or administration manager of a private school.

They are the people who decide if the school needs the solution and whether the school will pay for it.

The ideal customer is a small or medium private school that wants better organization, better parent communication, and better visibility over daily operations.

---

## 4. Main Users

### 4.1 Director / Admin

The director is the main user and decision-maker.

The director can:

* Manage students
* Manage classes
* Manage teachers
* Manage parents
* View attendance
* View payments
* View teacher notes
* View dashboard statistics

### 4.2 Teacher / Professor

The teacher uses the system for daily classroom operations.

The teacher can:

* View assigned classes
* Mark attendance by session/hour
* Add notes about students
* View students in assigned classes

### 4.3 Parent

The parent has an account and can log in to follow their children.

The parent can:

* View the list of their children
* Select a child
* View today’s attendance
* View the attendance calendar
* See if the child is currently present in class or not

### 4.4 Student

The student will not have an account in the MVP.

The student exists as a profile managed by the school.

A student account may be added later.

---

## 5. MVP Features

### 5.1 Authentication and Roles

The system will support different user roles:

* Director/Admin
* Teacher
* Parent

Each role will have access only to the features they need.

---

### 5.2 Student Management

The school can add and manage students.

Each student profile includes:

* Full name
* Class
* Parent/guardian
* Contact information
* Attendance history
* Payment status
* Teacher notes

---

### 5.3 Class Management

The school can create and manage classes.

Each class contains a list of students and can be assigned to teachers.

---

### 5.4 Timetable / Sessions

The school can create class sessions by day and time.

Example:

* Monday, 08:00–10:00, Mathematics
* Monday, 10:00–12:00, Arabic

This allows attendance to be tracked by session, not only by day.

---

### 5.5 Attendance by Session

Teachers can mark attendance for each session.

Attendance status can be:

* Present
* Absent
* Late
* Excused
* Not marked

This allows the parent and director to know the student’s real attendance status during the day.

---

### 5.6 Parent Dashboard

Parents can log in and see their children.

For each child, the parent can view:

* Today’s attendance
* Current class/session status
* Attendance calendar
* Present/absent/late status by session

The goal is to give parents visibility without depending  on WhatsApp messages.

---

### 5.7 Teacher Notes

Teachers can add notes about students.

Examples:

* Behavior note
* Homework note
* Performance note
* Discipline note
* General note

The director can view these notes from the dashboard or student profile.

---

### 5.8 Payment Tracking

The school can track student payments manually.

Payment status can be:

* Paid
* Unpaid
* Partial
* Late

The director can see unpaid students and payment summaries.

---

### 5.9 Director Dashboard

The director dashboard gives a clear overview of the school.

It should show:

* Total students
* Today’s attendance
* Absent students
* Late students
* Attendance not marked yet
* Unpaid students
* Latest teacher notes
* Class overview

This dashboard is one of the most important features because it helps sell the value of the platform.

---

## 6. First Market to Target

The first market to target is small and medium private schools in Morocco.

These schools are a good first market because:

* They usually need better organization.
* They communicate often with parents.
* They care about attendance and payment tracking.
* They may still use notebooks, Excel, and WhatsApp.
* The director can make decisions faster than in large institutions.

The first city or area should be local schools near the founder’s location, because they are easier to visit, interview, and follow up with.

---

## 7. Out of Scope for MVP

The following features are not part of the first MVP:

* Mobile app
* Real-time notifications
* Rral-time msg
* Student accounts
* Exam grades
* Homework management
* Online payments
* Advanced reports
* Multi-branch school support
* AI assistant
* Payroll management
* Transport management
* Library management

These features may be added later after the first MVP is validated.

---

## 8. Future Features After MVP

These features can be added after the MVP:

* Flutter mobile app
* Real-time notifications
* Real-time msg integration
* Student accounts
* Exam grades
* Homework
* Online payments
* Reports and analytics
* Multi-branch school support
* AI assistant for school administration

---

## 9. MVP Priority

The first MVP should focus on the most important daily problems:

1. User roles and authentication
2. Student management
3. Class management
4. Teacher-class assignment
5. Timetable/session management
6. Attendance by session
7. Parent attendance visibility
8. Teacher notes
9. Manual payment tracking
10. Director dashboard

The MVP should stay simple and focused.

The first goal is not to build a complete school ERP.

The first goal is to prove that schools want one clear system to track attendance, parent visibility, teacher notes, and payment status.
