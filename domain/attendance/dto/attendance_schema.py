from pydantic import BaseModel

class Attendance(BaseModel):
    id: int
    course_id: int
    student_id: int
    date: str
    check_in: str
    check_out: str
    status: str
    override_date: str
    override_time: str

class AttendanceContents(BaseModel):
    course_id: int
    student_id: int
    date: str
    check_in: str
    check_out: str
    status: str
    override_date: str
    override_time: str
