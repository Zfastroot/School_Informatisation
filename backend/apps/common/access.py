def get_user_school(user):
    if not user or not getattr(user, 'is_authenticated', False):
        return None
    return getattr(user, 'school', None)


def is_director(user):
    return bool(
        user
        and getattr(user, 'is_authenticated', False)
        and getattr(user, 'role', None) == 'director'
    )


def is_teacher(user):
    return bool(
        user
        and getattr(user, 'is_authenticated', False)
        and getattr(user, 'role', None) == 'teacher'
    )


def is_parent(user):
    return bool(
        user
        and getattr(user, 'is_authenticated', False)
        and getattr(user, 'role', None) == 'parent'
    )


def get_teacher_profile(user):
    if not is_teacher(user):
        return None
    return getattr(user, 'teacher_profile', None)


def get_parent_profile(user):
    if not is_parent(user):
        return None
    return getattr(user, 'parent_profile', None)


def get_object_school(obj):
    if obj is None:
        return None
    if obj.__class__.__name__ == 'School':
        return obj
    school = getattr(obj, 'school', None)
    if school is not None:
        return school
    user = getattr(obj, 'user', None)
    if user is not None:
        return getattr(user, 'school', None)
    student = getattr(obj, 'student', None)
    if student is not None:
        return getattr(student, 'school', None)
    classroom = getattr(obj, 'classroom', None)
    if classroom is not None:
        return getattr(classroom, 'school', None)
    timetable_session = getattr(obj, 'timetable_session', None)
    if timetable_session is not None:
        return getattr(timetable_session, 'school', None)
    return None


def same_school(user, obj):
    user_school = get_user_school(user)
    object_school = get_object_school(obj)
    return bool(user_school and object_school and user_school == object_school)


def teacher_has_class_access(user, classroom):
    teacher_profile = get_teacher_profile(user)
    if not teacher_profile or not classroom or not same_school(user, classroom):
        return False
    return teacher_profile.class_assignments.filter(classroom=classroom).exists()


def teacher_has_student_access(user, student):
    if not student or not same_school(user, student):
        return False
    return teacher_has_class_access(user, student.classroom)


def teacher_has_session_access(user, timetable_session):
    teacher_profile = get_teacher_profile(user)
    if not teacher_profile or not timetable_session or not same_school(user, timetable_session):
        return False
    return timetable_session.teacher_id == teacher_profile.id


def parent_has_student_access(user, student):
    parent_profile = get_parent_profile(user)
    if not parent_profile or not student or not same_school(user, student):
        return False
    return parent_profile.student_relations.filter(student=student).exists()


def teacher_has_object_access(user, obj):
    timetable_session = getattr(obj, 'timetable_session', None)
    if timetable_session is not None:
        return teacher_has_session_access(user, timetable_session)

    classroom = getattr(obj, 'classroom', None)
    if classroom is not None:
        return teacher_has_class_access(user, classroom)

    student = getattr(obj, 'student', None)
    if student is not None:
        return teacher_has_student_access(user, student)

    return False


def parent_has_object_access(user, obj):
    student = getattr(obj, 'student', None)
    if student is not None:
        return parent_has_student_access(user, student)
    return parent_has_student_access(user, obj)
