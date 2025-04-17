from fastapi import APIRouter, Body

from domain.taglog.dto import taglog_schema
from domain.taglog.service import taglog_service
from database import get_db
from fastapi import Depends


router = APIRouter(
    prefix="/api/taglog"
)

@router.get("/")
async def taglog_list(db  = Depends(get_db)):
    _taglog_list = await taglog_service.get_taglog_list(db)
    return _taglog_list

@router.get("/course/{course_id}")
async def taglog_in_course(course_id: int,
                           db  = Depends(get_db)):
    _taglog_in_course = await taglog_service.get_taglog_in_course(course_id, db)
    return _taglog_in_course

@router.get("/student/{student_id}")
async def taglog_in_student(student_id: int, db  = Depends(get_db)):
    _taglog_in_student = await taglog_service.get_taglog_in_student(student_id, db)
    return _taglog_in_student

@router.post("/")
async def tag(uid: str = Body(...), db  = Depends(get_db)):
    _taglog= await taglog_service.tag(uid,db)
    return _taglog
