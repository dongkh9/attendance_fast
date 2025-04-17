from sqlalchemy import select

from models import Attendance
from datetime import datetime
from sqlalchemy.orm import joinedload


async def get_today_attendance_list(today_str: str, db):
    query_result = await db.execute(
        select(Attendance)
        .where(Attendance.date == today_str)
        .options(
            joinedload(Attendance.student),
            joinedload(Attendance.course)
        )
    )
    records = query_result.scalars.all()

    def parse_time(t):
        if t is None:
            return datetime.min
        return datetime.strptime(t, "%H:%M:%S")

    records.sort(
        key=lambda r: max(parse_time(r.check_in), parse_time(r.check_out)),
        reverse=True
    )

    # ✅ dict로 가공하여 반환
    return [
        {
            "id": r.id,
            "course_id": r.course_id,
            "course_name": r.course.name if r.course else None,
            "student_id": r.student_id,
            "student_name": r.student.name if r.student else None,
            "date": r.date,
            "check_in": r.check_in,
            "check_out": r.check_out,
            "status": r.status,
            "override_date": r.override_date,
            "override_time": r.override_time,
        }
        for r in records
    ]


async def get_thatday_attendance_list(date_string, db):

    query_result = await db.execute(
        select(Attendance)
        .where(Attendance.date == date_string)
    )
    records = query_result.scalars.all()


    def parse_time(t):
        if t is None:
            return datetime.min
        return datetime.strptime(t, "%H:%M:%S")

    records.sort(
        key=lambda r: max(parse_time(r.check_in_time), parse_time(r.check_out_time)),
        reverse=True
    )
    return records

async def regist_attendance(_attendance_regist, db):
    new_attendance = Attendance(**_attendance_regist.dict())
    db.add(new_attendance)
    await db.commit()
    await db.refresh(new_attendance)
    return new_attendance

async def update_attendance(_attendance_update, id, db):
    query_result = await db.execute(
        select(Attendance)
        .where(Attendance.id == id)
    )
    attendance = query_result.scalar_one()
    for key, value in _attendance_update.dict(exclude_unset=True).items():
        setattr(attendance,key,value)
    await db.commit()
    await db.refresh(attendance)
    return attendance

async def delete_attendance(id, db):
    query_result = db.execute(
        select(Attendance)
        .where(Attendance.id == id)
    )
    attendance = query_result.scalar_one()
    await db.delete(attendance)
    await db.commit()


async def regist_nfc_attendance(taged_info, db):
    dt = datetime.fromisoformat(taged_info.tag_time)
    time_str = dt.strftime("%H:%M:%S")
    taged_info.tag_time = time_str
    query_result = await db.execute(
        select(Attendance)
        .where(Attendance.student_id == taged_info.student_id,
               Attendance.date == taged_info.date)
    )
    today_attendance = query_result.scalar_one_or_none()

    if today_attendance is None :
        new_attendance = Attendance(
            student_id= taged_info.student_id,
            course_id= taged_info.course_id,
            date= taged_info.date,
            check_in= taged_info.tag_time,
            status= "입실"
        )
        db.add(new_attendance)
        await db.commit()
        await db.refresh(new_attendance)
        return new_attendance
    elif today_attendance.check_out is None :
        setattr(today_attendance,"check_out",taged_info.tag_time)
        setattr(today_attendance,"status","퇴실")
        await db.commit()
        await db.refresh(today_attendance)
        return today_attendance
    else:
        return False