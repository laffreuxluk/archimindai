FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier tout le code (incluant launch.py)
COPY . .

EXPOSE 8000

# Définir PORT par défaut à 8000 (Railway pourra le redéfinir s'il le souhaite)
ENV PORT 8000

# Utiliser la forme shell : lancer l'application via launch.py
CMD python launch.py
