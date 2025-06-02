from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.core import serializers
import json

class Command(BaseCommand):
    help = 'Safely loads initial_data.json using update_or_create to avoid duplicates'

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

            loaded = 0
            for obj in serializers.deserialize("json", json.dumps(fixture_data)):
                model = obj.object.__class__
                fields = obj.object.__dict__.copy()
                fields.pop('_state', None)
                
                if hasattr(obj.object, 'code'):  # for ClassLevel and similar
                    # Remove 'code' from defaults to avoid constraint violations
                    code_value = fields.pop('code')
                    model.objects.update_or_create(
                        code=code_value, 
                        defaults=fields
                    )
                else:
                    # Remove 'id' from defaults if it exists
                    pk_value = fields.pop('id', obj.object.pk)
                    model.objects.update_or_create(
                        pk=pk_value, 
                        defaults=fields
                    )
                loaded += 1

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded or updated {loaded} objects!'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
            # Add more detailed error info for debugging
            import traceback
            self.stderr.write(self.style.ERROR(f'Traceback: {traceback.format_exc()}'))

        finally:
            if is_sqlite:
                cursor.execute('PRAGMA foreign_keys = ON;')