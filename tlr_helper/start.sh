#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Loading initial fixture data..."
python manage.py loaddata suggestor/fixtures/initial_data.json || echo "Fixture load skipped (error or already loaded)"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn core.wsgi:application
