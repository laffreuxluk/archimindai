from fastapi import FastAPI
from app.routes import data_processing, anomalies, reports

app = FastAPI(
    title="ArchimindAI",
    description="API pour le traitement de fichiers CSV et l'analyse avancée",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message": "Bienvenue sur ArchimindAI"}

app.include_router(data_processing.router, prefix="/data", tags=["Data Processing"])
app.include_router(anomalies.router, prefix="/anomalies", tags=["Anomalies"])
app.include_router(reports.router, prefix="/reports", tags=["Rapports"])
