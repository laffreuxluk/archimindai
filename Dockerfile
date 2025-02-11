FROM python:3.9-slim

WORKDIR /app

# Copier le fichier de dépendances et installer
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du code de l'application
COPY . .

EXPOSE 8000

# Lancer l'application en écoutant sur le port fixe 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
