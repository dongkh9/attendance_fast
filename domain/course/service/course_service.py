from domain.course.repository import course_crud

def get_course_list(db):
    course_list = course_crud.get_course_list(db)
    return course_list

def get_course_detail(id,db):
    course_detail = course_crud.get_course_detail(id, db)
    return course_detail


def regist_course(_course_regist,db):
    new_course = course_crud.regist_course(_course_regist, db)
    return new_course


def update_course(_course_update, id, db):
    updated_course = course_crud.update_course(_course_update, id, db)
    return updated_course


def delete_course(id, db):
    course_crud.delete_course(id,db)