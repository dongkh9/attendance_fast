from models import Attendance
from datetime import datetime
from sqlalchemy.orm import Session, joinedload


def get_today_attendance_list(today_str: str, db: Session):
    records = db.query(Attendance).filter(
        Attendance.date == today_str
    ).options(
        joinedload(Attendance.student),
        joinedload(Attendance.course)
    ).all()

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


def get_thatday_attendance_list(date_string, db):
    records = db.query(Attendance).filter(
        Attendance.date == date_string
    ).all()

    def parse_time(t):
        if t is None:
            return datetime.min
        return datetime.strptime(t, "%H:%M:%S")

    records.sort(
        key=lambda r: max(parse_time(r.check_in_time), parse_time(r.check_out_time)),
        reverse=True
    )
    return records

def regist_attendance(_attendance_regist, db):
    new_attendance = Attendance(**_attendance_regist.dict())
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

def update_attendance(_attendance_update, id, db):
    attendance = db.query(Attendance).filter(Attendance.id == id).first()
    for key, value in _attendance_update.dict(exclude_unset=True).items():
        setattr(attendance,key,value)
    db.commit()
    db.refresh(attendance)
    return attendance

def delete_attendance(id, db):
    attendance = db.query(Attendance).filter(Attendance.id == id).first()
    db.delete(attendance)
    db.commit()


def regist_nfc_attendance(taged_info, db):
    dt = datetime.fromisoformat(taged_info.tag_time)
    time_str = dt.strftime("%H:%M:%S")
    taged_info.tag_time = time_str
    today_attendance = db.query(Attendance).filter(Attendance.student_id == taged_info.student_id,
                                                   Attendance.date == taged_info.date).first()
    if today_attendance is None :
        new_attendance = Attendance(
            student_id= taged_info.student_id,
            course_id= taged_info.course_id,
            date= taged_info.date,
            check_in= taged_info.tag_time,
            status= "입실"
        )
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return new_attendance
    elif today_attendance.check_out is None :
        setattr(today_attendance,"check_out",taged_info.tag_time)
        setattr(today_attendance,"status","퇴실")
        db.commit()
        db.refresh(today_attendance)
        return today_attendance
    else:
        return False