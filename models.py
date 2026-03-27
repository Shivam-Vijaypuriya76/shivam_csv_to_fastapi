from sqlalchemy import Column, Integer, String
from database import Base

class UserModel(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key = True, index= True)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    major = Column(String(50), nullable=False)
    gpa = Column(Integer, nullable=False)
    attendance = Column(Integer, nullable=False)
    scholarship = Column(Integer,nullable=False)
    city = Column(String(50),nullable=False)
    status = Column(String(50), nullable=False)
