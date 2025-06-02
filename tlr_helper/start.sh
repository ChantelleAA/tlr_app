#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Loading initial fixture data..."
python manage.py load_fixtures_safe  || echo "Fixture load skipped (error or already loaded)"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn core.wsgi:application
