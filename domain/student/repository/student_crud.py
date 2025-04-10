from models import Student
from sqlalchemy.orm import Session

def get_student_in_course_list(course_id, db: Session):
    student_in_course_list = db.query(Student).filter(Student.course_id == course_id).all()
    return student_in_course_list


def get_student_list(db: Session):
    student_list = db.query(Student).all()
    return student_list


def get_student_detial(id, db):
    student_detail = db.query(Student).filter(Student.id == id).first()
    return student_detail


def regist_student(_student_regist, db):
    registed_student = Student(**_student_regist.dict())
    db.add(registed_student)
    db.commit()
    db.refresh(registed_student)
    return registed_student

def update_student(_student_update, id, db):
    student = db.query(Student).filter(Student.id == id).first()
    for key, value in _student_update.dict(exclude_unset=True).items():
        setattr(student, key, value)
    return student

def delete_student(id, db):
    student = db.query(Student).filter(Student.id == id).first()
    db.delete(student)
    db.commit()
