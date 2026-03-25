from fastapi import FastAPI
import pandas as pd

app = FastAPI()

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