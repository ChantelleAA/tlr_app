from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction
import json

class Command(BaseCommand):
    help = 'Load fixtures safely without foreign key constraint checks'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        try:
            # For SQLite, disable foreign key checks
            cursor.execute('PRAGMA foreign_keys = OFF;')
            
            self.stdout.write('Loading initial_data.json...')
            
            # Load fixtures without transaction (to avoid FK check re-enabling)
            with open('suggestor/fixtures/initial_data.json', 'r') as f:
                fixture_data = json.load(f)
            
            from django.core import serializers
            for obj in serializers.deserialize("json", json.dumps(fixture_data)):
                obj.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(fixture_data)} objects!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
        finally:
            # Re-enable foreign key checks
            cursor.execute('PRAGMA foreign_keys = ON;')