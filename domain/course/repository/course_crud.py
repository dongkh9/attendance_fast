from sqlalchemy import select,func

from models import Course, Student


# result = await db.execute(
#     select(Course.id, Course.name, func.count(Student.id).label("student_count"))
#     .outerjoin(Student, Student.course_id == Course.id)
#     .group_by(Course.id)
# )
async def get_course_list(db ):
    query_result = await db.execute(
        select(
            Course.id,
            Course.name,
            Course.manager,
            Course.start_date,
            Course.end_date,
            Course.start_time,
            Course.end_time,
            Course.order,
            Course.week_days,
            func.count(Student.id).label("student_count")
        )
        .outerjoin(Student, Student.course_id == Course.id)
        .group_by(Course.id)
        .order_by(Course.start_date.desc())
    )

    rows = query_result.all()
    course_list = [
        {
            "id": row[0],
            "name": row[1],
            "manager": row[2],
            "start_date": row[3],
            "end_date": row[4],
            "start_time": row[5],
            "end_time": row[6],
            "order": row[7],
            "week_days": row[8],
            "student_count": row[9]
        }
        for row in rows
    ]

    return course_list


async def get_course_detail(course_id: int, db ):
    query_result = await db.execute(
        select(Course)
        .where(Course.id == course_id)
    )
    return query_result.scalar_one_or_none()

async def regist_course(_course_regist, db):
    new_course = Course(**_course_regist.dict(exclude={"week_days"}))
    setattr(new_course, "week_days", ",".join(_course_regist.week_days))
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