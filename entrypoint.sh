#!/bin/sh

echo "Apply migrations"
alembic -c ../src/models/alembic.ini upgrade head

echo "Start API..."
uvicorn main:app --host 0.0.0.0 --port 8000
