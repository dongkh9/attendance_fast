from fastapi import APIRouter
from domain.course.dto import course_schema
from domain.course.service import course_service
from database import get_db
from fastapi import Depends

router = APIRouter(
    prefix="/api/course"
)

@router.get("/list", response_model=list[course_schema.Course])
async def course_list(db  = Depends(get_db)):
    _course_list = await course_service.get_course_list(db)
    return _course_list

@router.get("/{id}")
async def course_detail(id: int, db  = Depends(get_db)):
    _course_detail = await course_service.get_course_detail(id, db)
    return _course_detail

@router.post("/")
async def course_regist_manual(_course_regist: course_schema.CourseContents,
                         db  = Depends(get_db)):
    new_course = await course_service.regist_course(_course_regist,db)
    return new_course

@router.put("/{id}")
async def course_update(id: int,
                  _course_update: course_schema.CourseContents,
                  db  = Depends(get_db)):
    update_course = await course_service.update_course(_course_update, id, db)
    return update_course

@router.delete("/{id}")
async def course_delete(id: int, db  = Depends(get_db)):
    await course_service.delete_course(id,db)
