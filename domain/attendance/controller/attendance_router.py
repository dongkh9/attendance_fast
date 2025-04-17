from fastapi import APIRouter

from domain.attendance.dto import attendance_schema
from domain.attendance.service import attendance_service
from database import get_db
from fastapi import Depends

router = APIRouter(
    prefix="/api/attendance"
)

@router.get("/list/today", response_model=list[attendance_schema.AttendancePlus])
async def today_attendance_list(db  = Depends(get_db)):
    _today_attendance_list = await attendance_service.get_today_attendance_list(db)
    return _today_attendance_list

@router.get("/list/{date_string}")
async def thatday_attendance_list(date_string: str, db  = Depends(get_db)):
    _thatday_attendance_list = await attendance_service.get_thatday_attendance_list(date_string, db)
    return _thatday_attendance_list

@router.post("/")
async def regist_attendance(_attendance_regist: attendance_schema.AttendanceContents,
                         db  = Depends(get_db)):
    new_attendance = await attendance_service.regist_attendance(_attendance_regist,db)
    return new_attendance

@router.post("/nfc")
async def nfc_attendance(taged_info: attendance_schema.TagInfo,
                   db  = Depends(get_db)):
    new_attendacne = await attendance_service.nfc_attendance(taged_info,db)
    return new_attendacne


@router.put("/{id}")
async def attendance_update(id: int,
                      _attendance_update: attendance_schema.AttendanceContents,
                  db  = Depends(get_db)):
    update_attendance = await attendance_service.update_attendance(_attendance_update, id, db)
    return update_attendance

@router.delete("/{id}")
async def attendance_delete(id: int,
                      db  = Depends(get_db)):
    await attendance_service.delete_attendance(id,db)
