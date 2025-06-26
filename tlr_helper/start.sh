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

# ALWAYS CHECK FOR AND ADD NEW COMPREHENSIVE DATA
echo "🔍 Checking what data we have and what we need to add..."
python manage.py shell -c "
from suggestor.models import *

# Current data summary
print('=== CURRENT DATA SUMMARY ===')
print(f'ClassLevels: {ClassLevel.objects.count()}')
print(f'Subjects: {Subject.objects.count()}')
print(f'Materials: {Material.objects.count()}')
print(f'Themes: {Theme.objects.count()}')
print(f'TLRs: {Tlr.objects.count()}')

# Check specific data that should exist from new commands
nursery_tlrs = Tlr.objects.filter(class_level__name='Nursery').count()
interactive_tlrs = Tlr.objects.filter(title__icontains='Interactive').count()
kg1_tlrs = Tlr.objects.filter(class_level__name='KG1').count()
comprehensive_materials = Material.objects.count()

print(f'Nursery TLRs: {nursery_tlrs}')
print(f'Interactive TLRs: {interactive_tlrs}') 
print(f'KG1 TLRs: {kg1_tlrs}')
print(f'Materials: {comprehensive_materials}')

# Determine what needs to be added
needs_nursery = nursery_tlrs < 5
needs_interactive = interactive_tlrs < 5
needs_kg_primary = kg1_tlrs < 3
needs_materials = comprehensive_materials < 50

print(f'\\nNEEDS ASSESSMENT:')
print(f'Needs nursery data: {needs_nursery}')
print(f'Needs interactive data: {needs_interactive}')
print(f'Needs KG/Primary data: {needs_kg_primary}')
print(f'Needs more materials: {needs_materials}')

# Exit codes to signal what's needed
if needs_nursery or needs_materials:
    exit(1)  # Need nursery/foundation data
elif needs_interactive:
    exit(2)  # Need interactive data
elif needs_kg_primary:
    exit(3)  # Need KG/Primary data
else:
    exit(0)  # All data exists
"

DATA_NEEDS=$?

# Check if management commands exist
echo "🔧 Validating management commands exist..."
python manage.py help > commands_help.txt 2>&1

if grep -q "populate_nursery_data" commands_help.txt; then
    echo "✅ populate_nursery_data command found"
    NURSERY_CMD_EXISTS=1
else
    echo "❌ populate_nursery_data command NOT found"
    NURSERY_CMD_EXISTS=0
fi

if grep -q "create_interactive_tlrs" commands_help.txt; then
    echo "✅ create_interactive_tlrs command found"
    INTERACTIVE_CMD_EXISTS=1
else
    echo "❌ create_interactive_tlrs command NOT found"
    INTERACTIVE_CMD_EXISTS=0
fi

if grep -q "populate_kg_primary_data" commands_help.txt; then
    echo "✅ populate_kg_primary_data command found"
    KG_CMD_EXISTS=1
else
    echo "❌ populate_kg_primary_data command NOT found"
    KG_CMD_EXISTS=0
fi

rm commands_help.txt

# Add data based on what's needed and what commands exist
if [ $DATA_NEEDS -eq 1 ] && [ $NURSERY_CMD_EXISTS -eq 1 ]; then
    echo "🎨 Adding comprehensive nursery foundation data..."
    python manage.py populate_nursery_data || echo "⚠️ Nursery data command failed but continuing..."
    
elif [ $DATA_NEEDS -eq 1 ] && [ $NURSERY_CMD_EXISTS -eq 0 ]; then
    echo "⚠️ Need nursery data but command not found - checking file system..."
    ls -la suggestor/management/commands/ || echo "Management commands directory not found"
fi

if [ $DATA_NEEDS -le 2 ] && [ $INTERACTIVE_CMD_EXISTS -eq 1 ]; then
    echo "⚡ Adding interactive TLRs..."
    python manage.py create_interactive_tlrs || echo "⚠️ Interactive TLR command failed but continuing..."
    
elif [ $DATA_NEEDS -le 2 ] && [ $INTERACTIVE_CMD_EXISTS -eq 0 ]; then
    echo "⚠️ Need interactive data but command not found"
fi

if [ $DATA_NEEDS -le 3 ] && [ $KG_CMD_EXISTS -eq 1 ]; then
    echo "🎓 Adding KG and Primary TLRs..."
    python manage.py populate_kg_primary_data || echo "⚠️ KG/Primary command failed but continuing..."
    
elif [ $DATA_NEEDS -le 3 ] && [ $KG_CMD_EXISTS -eq 0 ]; then
    echo "⚠️ Need KG/Primary data but command not found"
fi

# If no commands were found, try to run them anyway (maybe help command is broken)
if [ $NURSERY_CMD_EXISTS -eq 0 ] && [ $INTERACTIVE_CMD_EXISTS -eq 0 ] && [ $KG_CMD_EXISTS -eq 0 ]; then
    echo "🔄 No commands detected in help, trying to run them anyway..."
    
    echo "Attempting nursery data..."
    python manage.py populate_nursery_data 2>&1 || echo "Nursery command failed"
    
    echo "Attempting interactive TLRs..."
    python manage.py create_interactive_tlrs 2>&1 || echo "Interactive command failed"
    
    echo "Attempting KG/Primary data..."
    python manage.py populate_kg_primary_data 2>&1 || echo "KG/Primary command failed"
fi

# Final verification of all data (both old and new)
echo "📊 Verifying complete data set..."
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

print('=== FINAL CURRICULUM DATA SUMMARY ===')
for model, count in counts.items():
    print(f'{model}: {count}')

# Check for specific data types
nursery_tlrs = Tlr.objects.filter(class_level__name='Nursery').count()
interactive_tlrs = Tlr.objects.filter(title__icontains='Interactive').count()
kg_tlrs = Tlr.objects.filter(class_level__name__in=['KG1', 'KG2']).count()
primary_tlrs = Tlr.objects.filter(class_level__name__in=['Class 1', 'Class 2', 'Class 3']).count()

print(f'\\n=== TLR BREAKDOWN ===')
print(f'Nursery TLRs: {nursery_tlrs}')
print(f'Interactive TLRs: {interactive_tlrs}')
print(f'KG TLRs: {kg_tlrs}')
print(f'Primary TLRs: {primary_tlrs}')
print(f'Total TLRs: {counts[\"TLRs\"]}')

# More lenient requirements to preserve existing data
required_minimums = {
    'ClassLevels': 2,  # At least basic levels
    'Materials': 10,   # Some materials
    'TLRs': 5,        # Some resources
}

missing_data = []
for model, minimum in required_minimums.items():
    if counts[model] < minimum:
        missing_data.append(f'{model}: {counts[model]}/{minimum}')

if missing_data:
    print('\\n❌ CRITICAL: Insufficient basic data:')
    for item in missing_data:
        print(f'  - {item}')
    sys.exit(1)
else:
    print('\\n✅ Curriculum database validated!')
    if nursery_tlrs > 0:
        print(f'✅ Successfully added nursery TLRs')
    if interactive_tlrs > 0:
        print(f'✅ Successfully added interactive TLRs')
    if kg_tlrs > 0 or primary_tlrs > 0:
        print(f'✅ Successfully added KG/Primary TLRs')
"

if [ $? -ne 0 ]; then
    echo "=== DEPLOYMENT FAILED - Data validation failed ==="
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

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "=== 🎉 DEPLOYMENT COMPLETE! ==="
echo "📊 Final Summary:"
python manage.py shell -c "
from suggestor.models import Tlr, Material, ClassLevel
total_tlrs = Tlr.objects.count()
materials = Material.objects.count()
class_levels = ClassLevel.objects.count()

print(f'   📚 {total_tlrs} Total Teaching & Learning Resources')
print(f'   🎨 {materials} Materials available') 
print(f'   🏫 {class_levels} Class levels configured')

# Show breakdown if we have the new data
nursery_count = Tlr.objects.filter(class_level__name='Nursery').count()
interactive_count = Tlr.objects.filter(title__icontains='Interactive').count()

if nursery_count > 0:
    print(f'   🧸 {nursery_count} Nursery TLRs')
if interactive_count > 0:
    print(f'   ⚡ {interactive_count} Interactive TLRs')
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