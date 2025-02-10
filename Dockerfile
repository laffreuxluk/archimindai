FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du code
COPY . .

EXPOSE 8000

# Définir la variable d'environnement PORT par défaut
ENV PORT 8000

# Utiliser sh -c pour que la substitution de la variable PORT soit effectuée lors de l'exécution dans le conteneur.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
