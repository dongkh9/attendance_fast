from fastapi import APIRouter
from sqlalchemy.orm import Session

from domain.student.dto import student_schema
from domain.student.service import student_service
from database import get_db
from fastapi import Depends

router = APIRouter(
    prefix="/api/student"
)

@router.get("/")
def student_list(db: Session = Depends(get_db)):
    _student_list = student_service.get_studetn_list(db)
    return _student_list

@router.get("/course/{course_id}")
def student_in_course_list(course_id: int,
                           db: Session = Depends(get_db)):
    _student_in_course_list = student_service.get_student_in_course_list(course_id, db)
    return _student_in_course_list

@router.get("/{id}")
def stduent_detail(id: int, db: Session = Depends(get_db)):
    _student_detail = student_service.get_student_detail(id, db)
    return _student_detail

@router.post("/")
def student_regist_manual(_student_regist: student_schema.StudentContents,
                         db: Session = Depends(get_db)):
    new_student = student_service.regist_student(_student_regist,db)
    return new_student

@router.put("/{id}")
def student_update(id: int,
                  _student_update: student_schema.StudentContents,
                  db: Session = Depends(get_db)):
    update_course = student_service.update_student(_student_update, id, db)
    return update_course

@router.delete("/{id}")
def student_delete(id: int, db: Session = Depends(get_db)):
    student_service.delete_student(id,db)
