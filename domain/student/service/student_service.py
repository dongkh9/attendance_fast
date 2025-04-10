from domain.student.repository import student_crud

def get_student_in_course_list(course_id, db):
    student_in_course_list = student_crud.get_student_in_course_list(course_id,db)
    return student_in_course_list


def get_studetn_list(db):
    student_list = student_crud.get_student_list(db)
    return student_list


def get_student_detail(id, db):
    student_detail = student_crud.get_student_detial(id,db)
    return student_detail


def regist_student(_student_regist, db):
    new_student = student_crud.regist_student(_student_regist,db)
    return new_student


def update_student(_student_update, id, db):
    updated_student = student_crud.update_student(_student_update, id ,db)
    return updated_student

def delete_student(id, db):
    student_crud.delete_student(id,db)