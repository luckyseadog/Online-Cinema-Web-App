#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo $AUTH_DB_HOST

# Print the current working directory
pwd

# Run alembic migrations
alembic -c src/alembic.ini upgrade head

# Create superadmin
python3 src/commands.py create-superadmin

# Create roles
python3 src/commands.py create-roles

# Start the Uvicorn server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --app-dir src
