from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.course.controller import course_router
from domain.attendance.controller import attendance_router
from domain.student.controller import student_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course_router.router)
app.include_router(attendance_router.router)
app.include_router(student_router.router)