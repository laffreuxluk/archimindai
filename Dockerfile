FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copier l'ensemble du code
COPY . .

EXPOSE 8000

CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port \${PORT:-8000}"
