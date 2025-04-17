from sqlalchemy import select

from models import TagLog, Student, Course

async def get_taglog_list(db ):
    query_result = await db.execute(
        select(TagLog)
    )
    taglog_list = query_result.scalars().all()
    return taglog_list


async def get_taglog_in_course(course_id, db ):
    query_result = await db.execute(
        select(TagLog)
        .where(TagLog.course_id == course_id)
    )
    taglog_in_course_list = query_result.scalars().all()
    return taglog_in_course_list


async def get_taglog_in_student(student_id, db):
    query_result = await db.execute(
        select(TagLog)
        .where(TagLog.student_id == student_id)
    )
    taglog_in_student_list = query_result.scalars().all()
    return taglog_in_student_list

async def tag(uid, db):
    query_result = await db.execute(
        select(Student)
        .where(Student.uid == uid)
    )
    taged_student = query_result.scalar_one_or_none()
    if taged_student is None:
        return
    student_id = taged_student.id
    course_id = taged_student.course_id

    registed_taglog = TagLog(
        uid= uid,
        student_id= student_id,
        course_id= course_id,
        message= "정상태그"
    )
    db.add(registed_taglog)
    await db.commit()
    await db.refresh(registed_taglog)
    return registed_taglog