FROM python:3.9-slim

WORKDIR /app

# Copier le fichier de dépendances et installer
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

EXPOSE 8000

# Utiliser ENTRYPOINT pour lancer l'application sur le port fixe 8000
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
