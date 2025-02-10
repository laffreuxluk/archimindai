import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes import router as api_router
from threading import Thread
from app.file_watcher import start_watcher
import uvicorn

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

app = FastAPI(
    title="ArchimindAI",
    description="API complète pour l'analyse de CSV, génération de rapports, détection d'anomalies, et paiements.",
    version="1.0"
)

app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur l'API ArchimindAI. Consultez /docs pour la documentation Swagger."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Erreur non gérée: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Erreur interne du serveur."})

def start_background_tasks():
    watcher_thread = Thread(target=start_watcher, daemon=True)
    watcher_thread.start()
    logging.info("File watcher démarré en arrière-plan.")

@app.on_event("startup")
def startup_event():
    start_background_tasks()
    logging.info("Application ArchimindAI démarrée.")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
