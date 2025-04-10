from datetime import datetime

from models import TagLog
from sqlalchemy.orm import Session

def get_taglog_list(db: Session):
    taglog_list = db.query(TagLog).all()
    return taglog_list


def get_taglog_in_course(course_id, db: Session):
    taglog_in_course_list = db.query(TagLog).filter(TagLog.course_id == course_id).all()
    return taglog_in_course_list


def get_taglog_in_student(student_id, db):
    taglog_in_student_list = db.query(TagLog).filter(TagLog.student_id == student_id).all()
    return taglog_in_student_list


def tag(db):
    mock_tag = TagLog(
        id=1,
        tag_time=datetime.now(),
        uid="test_uid",
        student_id=None,
        course_id=None,
        status="success",
        message="테스트로그입니다"
    )
    return mock_tag