import datetime

from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    course_id: int
    company: str
    department: str
    position: str
    phone: str
    uid: str

class StudentContents(BaseModel):
    name: str
    course_id: int
    company: str
    department: str
    position: str
    phone: str
    uid: str
