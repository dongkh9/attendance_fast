from domain.course.repository import course_crud

async def get_course_list(db):
    course_list = await course_crud.get_course_list(db)
    return course_list

async def get_course_detail(id,db):
    course_detail = await course_crud.get_course_detail(id, db)
    return course_detail


async def regist_course(_course_regist,db):
    new_course = await course_crud.regist_course(_course_regist, db)
    return new_course


async def update_course(_course_update, id, db):
    updated_course = await course_crud.update_course(_course_update, id, db)
    return updated_course


async def delete_course(id, db):
    await course_crud.delete_course(id,db)