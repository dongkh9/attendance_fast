from domain.attendance.repository import attendance_crud
from datetime import date


def get_today_attendance_list(db):
    today = date.today().strftime("%y-%m-%d")
    today_attendance_list = attendance_crud.get_today_attendance_list(today,db)
    return today_attendance_list


def get_thatday_attendance_list(date_string, db):
    thatday_attendance_list = attendance_crud.get_thatday_attendance_list(date_string, db)
    return thatday_attendance_list

def regist_attendance_manual(_attendance_regist, db):
    new_attendance = attendance_crud.regist_attendance_manual(_attendance_regist,db)
    return new_attendance

def update_attendance(_attendance_update, id, db):
    updated_attendance = attendance_crud.update_attendance(_attendance_update,id,db)
    return updated_attendance


def delete_attendance(id, db):
    attendance_crud.delete_attendance(id,db)