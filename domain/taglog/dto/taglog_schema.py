from pydantic import BaseModel


class TagLog(BaseModel):
    id: int
    tag_time: str
    uid: str
    student_id: int
    course_id: int
    message: str

class TagLogContents(BaseModel):
    tag_time: str
    uid: str
    student_id: int
    course_id: int
    message: str

