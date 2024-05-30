import datetime

from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Integer, String, Text)
from sqlalchemy.orm import relationship

from .db_manager import Base


class Students(Base):
    """Keeps track of school students"""

    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    phone_num = Column(String(100), nullable=False)
    parent_phone = Column(String(100))
    birth_year = Column(Integer, nullable=False)

    classes = relationship(
        "Classes", secondary="students_classes", back_populates="students", lazy=True
    )
    invoices = relationship("Invoices", back_populates="student")


class Teachers(Base):
    """Keeps track of teachers"""

    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    phone_num = Column(String(100), nullable=False)
    hourly = Column(Float, nullable=False)
    hire_date = Column(Date, nullable=False)

    classes = relationship("Classes", back_populates="teacher")
    paychecks = relationship("Paychecks", back_populates="teacher")


class Classes(Base):
    """Keeps track of classes"""

    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    class_name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    class_size = Column(Integer, nullable=False)
    class_start = Column(DateTime, nullable=False)
    class_end = Column(DateTime, nullable=False)
    event_id = Column(String(150))
    description = Column(Text)
    frequency = Column(JSON)
    classes_number=Column(Integer)

    teacher = relationship("Teachers", back_populates="classes", uselist=False)
    students = relationship(
        "Students", secondary="students_classes", back_populates="classes", lazy=True
    )


class StudentsClasses(Base):
    """Many to many relationship between clases and students"""

    __tablename__ = "students_classes"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)


class Invoices(Base):
    """Keeps track of transactions"""

    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    invoice_date = Column(Date, nullable=False)
    description = Column(Text)
    payment_status = Column(Boolean, default=False)
    amount = Column(Float, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))

    student = relationship("Students", back_populates="invoices", uselist=False)


class Paychecks(Base):
    """Stores teacher paychecks"""

    __tablename__ = "paychecks"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    end_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    is_payed = Column(Boolean, default=False, nullable=False)
    description = Column(Text)
    total_hours = Column(Float, nullable=False)
    total_school_hours = Column(Float, nullable=False)
    hourly = Column(Float, nullable=False)
    date_created = Column(Date, default=datetime.datetime.now().date())

    teacher = relationship("Teachers", back_populates="paychecks", uselist=False)
