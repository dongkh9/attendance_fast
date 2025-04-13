from fastapi import APIRouter
from sqlalchemy.orm import Session

from domain.attendance.dto import attendance_schema
from domain.attendance.service import attendance_service
from database import get_db
from fastapi import Depends

router = APIRouter(
    prefix="/api/attendance"
)

@router.get("/list/today", response_model=list[attendance_schema.Attendance])
def today_attendance_list(db: Session = Depends(get_db)):
    _today_attendance_list = attendance_service.get_today_attendance_list(db)
    return _today_attendance_list

@router.get("/list/{date_string}")
def thatday_attendance_list(date_string: str, db: Session = Depends(get_db)):
    _thatday_attendance_list = attendance_service.get_thatday_attendance_list(date_string, db)
    return _thatday_attendance_list

@router.post("/")
def course_attendance(_attendance_regist: attendance_schema.AttendanceContents,
                         db: Session = Depends(get_db)):
    new_attendance = attendance_service.regist_attendance(_attendance_regist,db)
    return new_attendance

@router.put("/{id}")
def attendance_update(id: int,
                      _attendance_update: attendance_schema.AttendanceContents,
                  db: Session = Depends(get_db)):
    update_attendance = attendance_service.update_attendance(_attendance_update, id, db)
    return update_attendance

@router.delete("/{id}")
def attendance_delete(id: int,
                      db: Session = Depends(get_db)):
    attendance_service.delete_attendance(id,db)
