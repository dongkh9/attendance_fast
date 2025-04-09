from fastapi import APIRouter
from sqlalchemy.orm import Session

from domain.student.dto import student_schema
from domain.student.service import student_service
from database import get_db
from fastapi import Depends

router = APIRouter(
    prefix="/api/student"
)

@router.get("/course/{course_id}")
def student_in_course_list(course_id: int,
                           db: Session = Depends(get_db)):
    _student_in_course_list = student_service.get_student_in_course_list(course_id, db)
    return _student_in_course_list
#
# @router.get("/{id}")
# def course_detail(id: int, db: Session = Depends(get_db)):
#     _course_detail = course_service.get_course_detail(id, db)
#     return _course_detail
#
# @router.post("/")
# def course_regist_manual(_course_regist: course_schema.CourseContents,
#                          db: Session = Depends(get_db)):
#     new_course = course_service.regist_course(_course_regist,db)
#     return new_course
#
# @router.put("/{id}")
# def course_update(id: int,
#                   _course_update: course_schema.CourseContents,
#                   db: Session = Depends(get_db)):
#     update_course = course_service.update_course(_course_update, id, db)
#     return update_course
#
# @router.delete("/{id}")
# def course_delete(id: int, db: Session = Depends(get_db)):
#     course_service.delete_course(id,db)
