from typing import Optional

from pydantic import BaseModel

class Attendance(BaseModel):
    id: int
    course_id: int
    student_id: int
    date: str
    check_in: str
    check_out: Optional[str] = None
    status: Optional[str] = None
    override_date: Optional[str] = None
    override_time: Optional[str] = None

class AttendanceContents(BaseModel):
    course_id: int
    student_id: int
    date: str
    check_in: str
    check_out: Optional[str] = None
    status: Optional[str] = None
    override_date: Optional[str] = None
    override_time: Optional[str] = None

class AttendancePlus(BaseModel):
    id: int
    course_id: int
    course_name: str
    student_id: int
    student_name: str
    date: str
    phone: str
    check_in: str
    check_out: Optional[str] = None
    status: Optional[str] = None
    override_date: Optional[str] = None
    override_time: Optional[str] = None


class TagInfo(BaseModel):
    course_id: int
    student_id: int
    date: str
    tag_time: str