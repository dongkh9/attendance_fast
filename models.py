# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    manager = Column(String(100))
    start_time = Column(String(5))  # 'HH:MM'
    end_time = Column(String(5))    # 'HH:MM'
    start_date = Column(String(8)) #YY-MM-DD
    end_date = Column(String(8))
    order = Column(Integer) # n기
    week_days = Column(String(100)) # "mon,wed,sun"
    @property
    def is_active(self):
        today = datetime.now().date()
        end = datetime.strptime(self.end_date, "%Y-%m-%d").date()
        return today <= end

    students = relationship("Student", back_populates="course")
    attendances = relationship("Attendance", back_populates="course")
    taglogs = relationship("TagLog", back_populates="course")


# =========================
# 교육생 테이블
# =========================
class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    phone = Column(String(50))
    uid = Column(String(100), unique=True)

    course = relationship("Course", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")
    taglogs = relationship("TagLog", back_populates="student")


# =========================
# 출석 테이블
# =========================
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)

    date = Column(String(8))  # 'YY-MM-DD'
    check_in = Column(String(8))  # 'HH:MM:SS'
    check_out = Column(String(8), nullable=True)  # 'HH:MM:SS'
    status = Column(String(20)) # 입실, 출석, 지각, 조퇴, 결석

    override_date = Column(String(8), nullable=True)
    override_time = Column(String(8), nullable=True)

    course = relationship("Course", back_populates="attendances")
    student = relationship("Student", back_populates="attendances")


# =========================
# 태그이력 테이블
# =========================
class TagLog(Base):
    __tablename__ = "tag_log"

    id = Column(Integer, primary_key=True, index=True)
    tag_time = Column(DateTime, default=datetime.now)
    uid = Column(String(100))
    student_id = Column(Integer, ForeignKey("student.id"), nullable=True)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=True)
    message = Column(String(255))

    course = relationship("Course", back_populates="taglogs")
    student = relationship("Student", back_populates="taglogs")

