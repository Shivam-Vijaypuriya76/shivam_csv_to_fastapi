from sqlalchemy import Column, Integer, String, Float
from database import Base

class UserModel(Base):
    __tablename__ = "students"

    student_id = Column(String(20), primary_key=True, index=True)  # ✅ FIX

    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    major = Column(String(50))

    gpa = Column(Float)   # ✅ FIX (float hona chahiye)
    attendance = Column(Integer)
    scholarship = Column(Integer)

    city = Column(String(50))
    status = Column(String(50))