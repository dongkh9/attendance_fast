from sqlalchemy import select

from models import Course


async def get_course_list(db ):
    query_result = await db.execute(
        select(Course)
        .order_by(Course.start_date.desc())
    )
    course_list = query_result.scalars().all()

    return course_list


async def get_course_detail(course_id: int, db ):
    query_result = await db.execute(
        select(Course)
        .where(Course.id == course_id)
    )
    return query_result.scalar_one_or_none()


async def regist_course(_course_regist, db  ):
    new_course = Course(**_course_regist.dict())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


async def update_course(_course_update, id, db ):
    query_result = await db.execute(
        select(Course)
        .where(Course.id == id)
    )
    course = query_result.scalar_one_or_none()
    for key, value in _course_update.dict(exclude_unset=True).items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course

async def delete_course(id, db ):
    query_result = await db.execute(
        select(Course)
        .where(Course.id == id)
    )
    course = query_result.scalar_one_or_none()
    await db.delete(course)
    await db.commit()