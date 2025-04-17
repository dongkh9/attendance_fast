from sqlalchemy import select

from models import Student

async def get_student_in_course_list(course_id, db):
    query_result = await db.execute(
        select(Student)
        .where(Student.course_id == course_id)
    )
    student_in_course_list = query_result.scalars().all()
    return student_in_course_list


async def get_student_list(db):
    query_result = await db.execute(
        select(Student)
    )
    student_list = query_result.scalars().all()
    return student_list


async def get_student_detial(id, db):
    query_result = await db.execute(
        select(Student)
        .where(Student.id == id)
    )
    student_detail = query_result.scalar_one_or_none()
    return student_detail


async def regist_student(_student_regist, db):
    registed_student = Student(**_student_regist.dict())
    db.add(registed_student)
    await db.commit()
    await db.refresh(registed_student)
    return registed_student

async def update_student(_student_update, id, db):
    query_result = await db.execute(
        select(Student)
        .where(Student.id == id)
    )
    student = query_result.scalar_one_or_none()
    for key, value in _student_update.dict(exclude_unset=True).items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return student

async def delete_student(id, db):
    query_result = await db.execute(
        select(Student)
        .where(Student.id == id)
    )
    student = query_result.scalar_one_or_none()
    db.delete(student)
    await db.commit()
