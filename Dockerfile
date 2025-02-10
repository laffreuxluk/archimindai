FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du code (y compris start.sh)
COPY . .

EXPOSE 8000

# Définir une valeur par défaut pour PORT (Railway peut la redéfinir)
ENV PORT 8000

# Utiliser start.sh comme script de démarrage
CMD ["/bin/sh", "start.sh"]
