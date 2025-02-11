from fastapi import APIRouter

router = APIRouter()

@router.get("/detect")
def detect_anomalies():
    return {"message": "Anomalies détectées"}
