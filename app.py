from fastapi import FastAPI, HTTPException,Depends
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine, Base, get_db

import models  

app = FastAPI()


Base.metadata.create_all(bind=engine)

@app.get('/db-connect')
def connect_db():
    try:
        with engine.connect() as con:
            result = con.execute(text("SELECT 1"))
            return {
                "message": "Database connection successful",
                "result": result.fetchone()[0]
            }
    except Exception as e:
        return {
            "message": "Database connection failed",
            "error": str(e)
        }


@app.get("/")
def home():
    return {"message": "Hello FastAPI"}

@app.get("/get-csv-data")
def get_csv_data():

    try:
        df = pd.read_csv("students_complete.csv")

        return {
            "columns": list(df.columns),
            "total_rows": len(df),
            "data": df.fillna("").to_dict(orient="records")
        }

    except FileNotFoundError:
        return {
            "error": "students_complete.csv not found. Make sure it is in same folder as app.py"
        }

    except Exception as e:
        return {
            "error": str(e)
        }
    


# ✅ Get data by student_id (STRING type)
@app.get("/get-student/{student_id}")
def get_student_by_studentid(student_id: str):

    try:
        df = pd.read_csv("students_complete.csv")

        student = df[df["student_id"] == student_id]

        if student.empty:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return student.fillna("").to_dict(orient="records")[0]

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="CSV file not found"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    
@app.post("/upload-csv-to-db")
def upload_csv_to_db(db: Session = Depends(get_db)):
    try:
        df = pd.read_csv("students_complete.csv")

        for _, row in df.iterrows():

            existing = db.query(models.UserModel).filter(
                models.UserModel.student_id == row["student_id"]
            ).first()

            if existing:
                continue

            student = models.UserModel(
                student_id=row["student_id"],  # ✅ STRING

                first_name=row["first_name"],
                last_name=row["last_name"],

                age=None if pd.isna(row["age"]) else int(row["age"]),
                major=row["major"],
                gpa=None if pd.isna(row["gpa"]) else float(row["gpa"]),
                attendance=None if pd.isna(row["attendance"]) else int(row["attendance"]),
                scholarship=None if pd.isna(row["scholarship"]) else int(row["scholarship"]),

                city=row["city"],
                status=row["status"]
            )

            db.add(student)

        db.commit()

        return {"message": "CSV data successfully inserted into MySQL"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}