from fastapi import APIRouter

from domain.student.dto import student_schema
from domain.student.service import student_service
from database import get_db
from fastapi import Depends

router = APIRouter(
    prefix="/api/student"
)

@router.get("/")
async def student_list(db = Depends(get_db)):
    _student_list = await student_service.get_studetn_list(db)
    return _student_list

@router.get("/course/{course_id}")
async def student_in_course_list(course_id: int,
                           db = Depends(get_db)):
    _student_in_course_list = await student_service.get_student_in_course_list(course_id, db)
    return _student_in_course_list

@router.get("/{id}")
async def stduent_detail(id: int, db = Depends(get_db)):
    _student_detail = await student_service.get_student_detail(id, db)
    return _student_detail

@router.post("/")
async def student_regist_manual(_student_regist: student_schema.StudentContents,
                         db = Depends(get_db)):
    new_student = await student_service.regist_student(_student_regist,db)
    return new_student

@router.put("/{id}")
async def student_update(id: int,
                  _student_update: student_schema.StudentContents,
                  db = Depends(get_db)):
    update_course = await student_service.update_student(_student_update, id, db)
    return update_course

@router.delete("/{id}")
async def student_delete(id: int, db = Depends(get_db)):
    await student_service.delete_student(id,db)
