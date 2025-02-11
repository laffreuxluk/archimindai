from fastapi import APIRouter

router = APIRouter()

@router.get("/generate")
def generate_report():
    return {"message": "Rapport généré avec succès"}
