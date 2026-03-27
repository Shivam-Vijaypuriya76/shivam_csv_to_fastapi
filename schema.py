from pydantic import BaseModel, ConfigDict

# Create Schema (POST request ke liye)
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    major: str
    gpa: int
    attendance: int
    scholarship: int
    city: str
    status: str


# Response Schema (API response ke liye)
class StudentResponse(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    age: int
    major: str
    gpa: int
    attendance: int
    scholarship: int
    city: str
    status: str

    model_config = ConfigDict(from_attributes=True)