from fastapi import APIRouter

router = APIRouter()

@router.post("/clean")
def clean_data():
    return {"message": "Données nettoyées avec succès"}
