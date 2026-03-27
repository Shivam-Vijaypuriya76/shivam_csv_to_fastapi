from fastapi import FastAPI, HTTPException
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine, Base, get_db

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
    
    