from domain.taglog.repository import taglog_crud

def get_taglog_list(db):
    taglog_list = taglog_crud.get_taglog_list(db)
    return taglog_list


def get_taglog_in_course(course_id, db):
    taglog_in_course_list = taglog_crud.get_taglog_in_course(course_id,db)
    return taglog_in_course_list


def get_taglog_in_student(student_id, db):
    taglog_in_student_list = taglog_crud.get_taglog_in_student(student_id, db)
    return taglog_in_student_list


def tag(uid, db):
    tag_log = taglog_crud.tag(uid, db)
    return tag_log