from domain.attendance.repository import attendance_crud
from datetime import date


async def get_today_attendance_list(db):
    today = date.today().strftime("%y-%m-%d")
    today_attendance_list = await attendance_crud.get_today_attendance_list(today,db)
    return today_attendance_list


async def get_thatday_attendance_list(date_string, db):
    thatday_attendance_list = await attendance_crud.get_thatday_attendance_list(date_string, db)
    return thatday_attendance_list

async def regist_attendance(_attendance_regist, db):
    new_attendance = await attendance_crud.regist_attendance(_attendance_regist,db)
    return new_attendance

async def update_attendance(_attendance_update, id, db):
    updated_attendance = await attendance_crud.update_attendance(_attendance_update,id,db)
    return updated_attendance


async def delete_attendance(id, db):
    await attendance_crud.delete_attendance(id,db)


async def nfc_attendance(taged_info, db):
    new_attendnace = await attendance_crud.regist_nfc_attendance(taged_info,db)
    return new_attendnace