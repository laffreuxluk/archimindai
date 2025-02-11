#!/bin/bash
# Vérifier si la variable PORT est définie, sinon utiliser 8000
PORT=${PORT:-8000}

echo "🚀 Démarrage de l'application sur le port $PORT..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
