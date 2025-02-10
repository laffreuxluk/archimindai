import os
import uvicorn

# Récupère le port depuis l'environnement, ou utilise 8000 par défaut.
port = int(os.environ.get("PORT", 8000))
uvicorn.run("app.main:app", host="0.0.0.0", port=port)
