#!/bin/bash
# entrypoint.sh

# Wait for the database to be ready
./wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is up"

python manage.py seed_groups

gunicorn --bind 0.0.0.0:8000 app.wsgi:application