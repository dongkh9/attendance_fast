from domain.student.repository import student_crud

async def get_student_in_course_list(course_id, db):
    student_in_course_list = await student_crud.get_student_in_course_list(course_id,db)
    return student_in_course_list


async def get_studetn_list(db):
    student_list = await student_crud.get_student_list(db)
    return student_list


async def get_student_detail(id, db):
    student_detail = await student_crud.get_student_detial(id,db)
    return student_detail


async def regist_student(_student_regist, db):
    new_student = await student_crud.regist_student(_student_regist,db)
    return new_student


async def update_student(_student_update, id, db):
    updated_student = await student_crud.update_student(_student_update, id ,db)
    return updated_student

async def delete_student(id, db):
    await student_crud.delete_student(id,db)