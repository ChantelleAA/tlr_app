#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Clearing existing initial data if present..."
python manage.py shell -c "
from suggestor.models import ClassLevel
ClassLevel.objects.filter(code__in=['1','2','3','4','5','6','7']).delete()
"

echo "Loading initial fixture data..."
python manage.py load_fixtures_safe || echo "Fixture load skipped (error or already loaded)"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn core.wsgi:application
