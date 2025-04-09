from models import Attendance
from datetime import datetime
from sqlalchemy.orm import Session


def get_today_attendance_list(today_str: str, db: Session):
    records = db.query(Attendance).filter(
        Attendance.date == today_str
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

def regist_attendance_manual(_attendance_regist, db):
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