from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import connection
from django.conf import settings
import json

class Command(BaseCommand):
    help = 'Load fixtures safely without foreign key constraint checks (for SQLite only)'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        db_engine = settings.DATABASES['default']['ENGINE']
        is_sqlite = 'sqlite' in db_engine

        try:
            if is_sqlite:
                cursor.execute('PRAGMA foreign_keys = OFF;')

            self.stdout.write('Loading initial_data.json...')

            with open('suggestor/fixtures/initial_data.json', 'r') as f:
                fixture_data = json.load(f)

            for obj in serializers.deserialize("json", json.dumps(fixture_data)):
                obj.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(fixture_data)} objects!'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))

        finally:
            if is_sqlite:
                cursor.execute('PRAGMA foreign_keys = ON;')
