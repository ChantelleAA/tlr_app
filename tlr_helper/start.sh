#!/bin/bash

echo "=== Starting Render Deployment ==="

# First, ensure we have the latest migrations
echo "Making migrations..."
python manage.py makemigrations --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

# Wait a moment for migrations to complete
sleep 3

echo "Checking database schema..."
python manage.py shell -c "
from django.db import connection
from django.db import OperationalError

try:
    cursor = connection.cursor()
    # Use PostgreSQL-compatible syntax for Render
    cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name='suggestor_classlevel'\")
    columns = [row[0] for row in cursor.fetchall()]
    print('ClassLevel columns:', columns)
    
    # Check if we have any data
    cursor.execute(\"SELECT COUNT(*) FROM suggestor_classlevel\")
    count = cursor.fetchone()[0]
    print(f'ClassLevel records: {count}')
except OperationalError as e:
    print(f'Database check error: {e}')
"

# Load initial data using our custom command
echo "Loading initial curriculum data..."
python manage.py shell -c "
from suggestor.models import ClassLevel
if ClassLevel.objects.count() == 0:
    print('No initial data found. Loading from fixtures...')
    exit_code = 1  # Signal that we need to load fixtures
else:
    print('Initial data already exists. Skipping fixture loading.')
    exit_code = 0
exit(exit_code)
"

# Check the exit code and load fixtures if needed
if [ $? -eq 1 ]; then
    echo "Loading fixtures with custom command..."
    python manage.py load_fixtures_safe
    
    # Verify fixture loading was successful
    python manage.py shell -c "
from suggestor.models import ClassLevel, Subject, Strand, Tlr
print(f'ClassLevels loaded: {ClassLevel.objects.count()}')
print(f'Subjects loaded: {Subject.objects.count()}')
print(f'Strands loaded: {Strand.objects.count()}')
print(f'TLRs loaded: {Tlr.objects.count()}')
    "
fi

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
try:
    if not User.objects.filter(username='chantelle').exists():
        User.objects.create_superuser('chantelle', 'chantelle@example.com', '2241')
        print('Superuser chantelle created successfully')
    else:
        print('Superuser chantelle already exists')
except Exception as e:
    print(f'Error creating superuser: {e}')
"

# Optional: Create additional admin users from environment variables
if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_PASSWORD" ]; then
    echo "Creating additional admin user from environment..."
    python manage.py shell -c "
from django.contrib.auth.models import User
import os
username = os.environ.get('ADMIN_USERNAME')
password = os.environ.get('ADMIN_PASSWORD')
email = os.environ.get('ADMIN_EMAIL', f'{username}@example.com')

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f'Additional admin user {username} created successfully')
    else:
        print(f'Admin user {username} already exists')
except Exception as e:
    print(f'Error creating admin user: {e}')
    "
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run a final health check
echo "Running deployment health check..."
python manage.py shell -c "
from django.db import connection
from suggestor.models import ClassLevel
try:
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    
    # Test model access
    count = ClassLevel.objects.count()
    print(f'Health check passed. Database accessible with {count} class levels.')
    
    if count == 0:
        print('WARNING: No curriculum data loaded!')
        exit(1)
    else:
        print('Curriculum data successfully loaded.')
        
except Exception as e:
    print(f'Health check failed: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "=== DEPLOYMENT FAILED - Health check failed ==="
    exit 1
fi

echo "=== Deployment Complete Successfully ==="
echo "Starting Gunicorn server..."

# Start Gunicorn with proper configuration for Render
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --preload \
    --access-logfile - \
    --error-logfile -
