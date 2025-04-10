from fastapi import APIRouter
from sqlalchemy.orm import Session

from domain.taglog.dto import taglog_schema
from domain.taglog.service import taglog_service
from database import get_db
from fastapi import Depends


router = APIRouter(
    prefix="/api/taglog"
)

@router.get("/")
def taglog_list(db: Session = Depends(get_db)):
    _taglog_list = taglog_service.get_taglog_list(db)
    return _taglog_list

@router.get("/course/{course_id}")
def taglog_in_course(course_id: int,
                           db: Session = Depends(get_db)):
    _taglog_in_course = taglog_service.get_taglog_in_course(course_id, db)
    return _taglog_in_course

@router.get("/student/{student_id}")
def taglog_in_student(student_id: int, db: Session = Depends(get_db)):
    _taglog_in_student = taglog_service.get_taglog_in_student(student_id, db)
    return _taglog_in_student

@router.post("/")
def tag(db: Session = Depends(get_db)):
    _taglog= taglog_service.tag(db)
    return _taglog

