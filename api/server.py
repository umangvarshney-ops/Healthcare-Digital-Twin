from fastapi import FastAPI
from pydantic import BaseModel
from digital_twin.twin import DigitalTwin
import pandas as pd
app = FastAPI(
    title="Healthcare Digital Twin API"
)
@app.get("/")
# Home Route
def home():
    return {
        "message": "Healthcare Digital Twin API Running"
    }
# Health Route
@app.get("/health")
def health():
    return {
        "status": "running"
    }

# history
@app.get("/history")
def history():

    df = pd.read_csv("data/patient_history.csv")

    return df.tail(10).to_dict(orient="records")

class Patient(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

# Predict Route
@app.post("/predict")
def predict(patient: Patient):

    twin = DigitalTwin(
        age=patient.age,
        sex=patient.sex,
        cp=patient.cp,
        trestbps=patient.trestbps,
        chol=patient.chol,
        fbs=patient.fbs,
        restecg=patient.restecg,
        thalach=patient.thalach,
        exang=patient.exang,
        oldpeak=patient.oldpeak,
        slope=patient.slope,
        ca=patient.ca,
        thal=patient.thal
    )

    report = twin.generate_report()

    return report