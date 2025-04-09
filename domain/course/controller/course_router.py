from fastapi import APIRouter
from sqlalchemy.orm import Session

from domain.course.dto import course_schema
from domain.course.service import course_service
from database import get_db
from fastapi import Depends

router = APIRouter(
    prefix="/api/course"
)

@router.get("/list", response_model=list[course_schema.Course])
def course_list(db: Session = Depends(get_db)):
    _course_list = course_service.get_course_list(db)
    return _course_list

@router.get("/{id}")
def course_detail(id: int, db: Session = Depends(get_db)):
    _course_detail = course_service.get_course_detail(id, db)
    return _course_detail

@router.post("/")
def course_regist_manual(_course_regist: course_schema.CourseContents,
                         db: Session = Depends(get_db)):
    new_course = course_service.regist_course(_course_regist,db)
    return new_course

@router.put("/{id}")
def course_update(id: int,
                  _course_update: course_schema.CourseContents,
                  db: Session = Depends(get_db)):
    update_course = course_service.update_course(_course_update, id, db)
    return update_course

@router.delete("/{id}")
def course_delete(id: int, db: Session = Depends(get_db)):
    course_service.delete_course(id,db)
