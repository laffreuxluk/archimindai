#!/bin/sh
echo "Starting uvicorn with port ${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
