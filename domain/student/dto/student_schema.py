from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    course_id: int
    phone: str
    uid: str

class StudentContents(BaseModel):
    name: str
    course_id: int
    phone: str
    uid: str
