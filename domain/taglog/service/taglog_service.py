from domain.taglog.repository import taglog_crud

async def get_taglog_list(db):
    taglog_list = await taglog_crud.get_taglog_list(db)
    return taglog_list


async def get_taglog_in_course(course_id, db):
    taglog_in_course_list = await taglog_crud.get_taglog_in_course(course_id,db)
    return taglog_in_course_list


async def get_taglog_in_student(student_id, db):
    taglog_in_student_list = await taglog_crud.get_taglog_in_student(student_id, db)
    return taglog_in_student_list


async def tag(uid, db):
    tag_log = await taglog_crud.tag(uid, db)
    return tag_log