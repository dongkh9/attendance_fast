from datetime import datetime

from models import TagLog, Student, Course
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
    #
    # registed_student = Student(**_student_regist.dict())
    # db.add(registed_student)
    # db.commit()
    # db.refresh(registed_student)

def tag(uid, db):
    taged_student = db.query(Student).filter(Student.uid == uid).first()
    if taged_student is None:
        return
    student_id = taged_student.id
    course_id = taged_student.course_id

    registed_taglog = TagLog(
        uid= uid,
        student_id= student_id,
        course_id= course_id,
        message= "정상태그"
    )
    db.add(registed_taglog)
    db.commit()
    db.refresh(registed_taglog)
    return registed_taglog