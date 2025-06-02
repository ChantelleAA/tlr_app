#!/bin/bash

echo "=== Starting Deployment ==="

# First, ensure we have the latest migrations
echo "Making migrations..."
python manage.py makemigrations --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

# Wait a moment for migrations to complete
sleep 2

echo "Checking database schema..."
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name='suggestor_classlevel'\")
print('ClassLevel columns:', [row[0] for row in cursor.fetchall()])
"

# Skip fixture loading for now - let the post_migrate signal handle it
echo "Skipping fixture loading - using post_migrate signal instead"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Deployment Complete ==="
echo "Starting Gunicorn..."
gunicorn core.wsgi:application