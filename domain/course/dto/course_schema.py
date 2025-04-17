from typing import List

from pydantic import BaseModel

class Course(BaseModel):
    id: int
    name: str
    manager: str
    start_time: str
    end_time: str
    start_date: str
    end_date: str
    order: int
    week_days: str
    student_count: int


class CourseContents(BaseModel):
    name: str
    manager: str
    start_time: str
    end_time: str
    start_date: str
    end_date: str
    order: int
    week_days: List[str]

