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

# Load initial data using our new management commands
echo "Checking for existing curriculum data..."
python manage.py shell -c "
from suggestor.models import ClassLevel, Tlr, Material
class_count = ClassLevel.objects.count()
tlr_count = Tlr.objects.count()
material_count = Material.objects.count()

print(f'ClassLevels: {class_count}')
print(f'TLRs: {tlr_count}')
print(f'Materials: {material_count}')

if class_count == 0 or material_count == 0:
    print('NEED_BASIC_DATA')
    exit(1)
elif tlr_count < 5:  # If we have less than 5 TLRs, load more
    print('NEED_MORE_TLRS')
    exit(2)
else:
    print('DATA_EXISTS')
    exit(0)
"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 1 ]; then
    echo "Loading comprehensive nursery data..."
    python manage.py populate_nursery_data
    
    # Verify basic data loading
    python manage.py shell -c "
from suggestor.models import ClassLevel, Subject, Material, Tlr
print(f'ClassLevels loaded: {ClassLevel.objects.count()}')
print(f'Subjects loaded: {Subject.objects.count()}')
print(f'Materials loaded: {Material.objects.count()}')
print(f'Basic TLRs loaded: {Tlr.objects.count()}')
    "
    
    echo "Loading interactive TLRs..."
    python manage.py create_interactive_tlrs
    
elif [ $EXIT_CODE -eq 2 ]; then
    echo "Basic data exists, loading additional interactive TLRs..."
    python manage.py create_interactive_tlrs
    
else
    echo "All curriculum data already exists, skipping data loading..."
fi

# Final verification of all data
echo "Verifying complete data set..."
python manage.py shell -c "
from suggestor.models import *
import sys

# Count all major models
counts = {
    'ClassLevels': ClassLevel.objects.count(),
    'Subjects': Subject.objects.count(),
    'Materials': Material.objects.count(),
    'Themes': Theme.objects.count(),
    'Learning Styles': LearningStyle.objects.count(),
    'Special Needs': SpecialNeed.objects.count(),
    'TLRs': Tlr.objects.count(),
    'Strands': Strand.objects.count(),
}

print('=== CURRICULUM DATA SUMMARY ===')
for model, count in counts.items():
    print(f'{model}: {count}')

# Check for nursery-specific data
nursery_tlrs = Tlr.objects.filter(class_level__name='Nursery').count()
interactive_tlrs = Tlr.objects.filter(title__icontains='Interactive').count()

print(f'Nursery TLRs: {nursery_tlrs}')
print(f'Interactive TLRs: {interactive_tlrs}')

# Verify we have minimum required data
required_minimums = {
    'ClassLevels': 2,  # At least Creche and Nursery
    'Materials': 20,   # Comprehensive materials list
    'TLRs': 10,       # Good collection of resources
}

missing_data = []
for model, minimum in required_minimums.items():
    if counts[model] < minimum:
        missing_data.append(f'{model}: {counts[model]}/{minimum}')

if missing_data:
    print('WARNING: Insufficient data loaded:')
    for item in missing_data:
        print(f'  - {item}')
    sys.exit(1)
else:
    print('✅ All curriculum data successfully loaded!')
"

if [ $? -ne 0 ]; then
    echo "=== DEPLOYMENT FAILED - Curriculum data loading failed ==="
    exit 1
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

# Check if we can run the management commands (validate they exist)
echo "Validating management commands..."
python manage.py help | grep -E "(populate_nursery_data|create_interactive_tlrs)" > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Custom management commands available"
else
    echo "⚠️  Warning: Custom management commands not found - check directory structure"
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run a comprehensive health check
echo "Running deployment health check..."
python manage.py shell -c "
from django.db import connection
from suggestor.models import *
import sys

try:
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('✅ Database connection successful')
    
    # Test model access and data integrity
    class_levels = ClassLevel.objects.count()
    subjects = Subject.objects.count()
    tlrs = Tlr.objects.count()
    materials = Material.objects.count()
    
    print(f'✅ Models accessible:')
    print(f'   - Class Levels: {class_levels}')
    print(f'   - Subjects: {subjects}') 
    print(f'   - TLRs: {tlrs}')
    print(f'   - Materials: {materials}')
    
    # Test relationships
    nursery_subjects = Subject.objects.filter(class_level__name='Nursery').count()
    print(f'   - Nursery subjects: {nursery_subjects}')
    
    # Test TLR relationships
    tlrs_with_materials = Tlr.objects.filter(materials__isnull=False).distinct().count()
    print(f'   - TLRs with materials: {tlrs_with_materials}')
    
    if class_levels == 0:
        print('❌ CRITICAL: No curriculum data loaded!')
        sys.exit(1)
    elif tlrs < 5:
        print('⚠️  WARNING: Very few TLRs loaded')
        sys.exit(1)
    else:
        print('✅ Comprehensive curriculum data successfully loaded!')
        
except Exception as e:
    print(f'❌ Health check failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "=== DEPLOYMENT FAILED - Health check failed ==="
    exit 1
fi

echo "=== 🎉 Deployment Complete Successfully ==="
echo "📊 Curriculum Summary:"
python manage.py shell -c "
from suggestor.models import Tlr, Material, ClassLevel
print(f'   📚 {Tlr.objects.count()} Teaching & Learning Resources loaded')
print(f'   🎨 {Material.objects.count()} Materials available')
print(f'   🏫 {ClassLevel.objects.count()} Class levels configured')
print(f'   🎯 {Tlr.objects.filter(class_level__name=\"Nursery\").count()} Nursery-specific TLRs')
print(f'   ⚡ {Tlr.objects.filter(title__icontains=\"Interactive\").count()} Interactive TLRs')
"

echo "🚀 Starting Gunicorn server..."

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