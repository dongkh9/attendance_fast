from models import Course
from sqlalchemy.orm import Session


def get_course_list(db: Session):
    course_list = db.query(Course)\
    .order_by(Course.start_date.desc())\
    .all()
    return course_list


def get_course_detail(course_id: int, db: Session):
    return db.query(Course).filter(Course.id == course_id).first()


def regist_course(_course_regist, db: Session ):
    new_course = Course(**_course_regist.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


def update_course(_course_update, id, db: Session):
    course = db.query(Course).filter(Course.id == id).first()
    for key, value in _course_update.dict(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

def delete_course(id, db: Session):
    course = db.query(Course).filter(Course.id == id).first()
    db.delete(course)
    db.commit()