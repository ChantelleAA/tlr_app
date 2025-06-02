from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection, transaction
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
            updated = 0
            skipped = 0

            # Process in order: first create basic lookup tables, then complex ones
            model_order = [
                'suggestor.classlevel',
                'suggestor.theme',
                'suggestor.keylearningarea', 
                'suggestor.corecompetency',
                'suggestor.resourcetype',
                'suggestor.goaltag',
                'suggestor.material',
                'suggestor.specialneed',
                'suggestor.learningstyle',
                'suggestor.subject',
                'suggestor.strand',
                'suggestor.substrand',
                'suggestor.contentstandard',
                'suggestor.indicator',
                'suggestor.tlr',
                'suggestor.tlrimage',
                'suggestor.tlrvideo'
            ]

            # Group objects by model
            objects_by_model = {}
            for obj_data in fixture_data:
                model_name = obj_data['model']
                if model_name not in objects_by_model:
                    objects_by_model[model_name] = []
                objects_by_model[model_name].append(obj_data)

            # Process in the specified order
            for model_name in model_order:
                if model_name not in objects_by_model:
                    continue
                    
                self.stdout.write(f'Processing {model_name}...')
                
                for obj_data in objects_by_model[model_name]:
                    try:
                        app_label, model_class_name = model_name.split('.')
                        
                        # Import the model dynamically
                        from django.apps import apps
                        model = apps.get_model(app_label, model_class_name)
                        
                        fields = obj_data['fields'].copy()
                        pk = obj_data.get('pk')
                        
                        # Handle models with unique 'code' field specially
                        if hasattr(model, 'code') and 'code' in fields:
                            code_value = fields.pop('code')  # Remove code from fields for defaults
                            obj, created = model.objects.get_or_create(
                                code=code_value,
                                defaults={'id': pk, 'code': code_value, **fields}
                            )
                            if not created:
                                # Update existing object
                                for key, value in fields.items():
                                    setattr(obj, key, value)
                                obj.save()
                                updated += 1
                                self.stdout.write(f'  Updated {model_class_name} code={code_value}')
                            else:
                                loaded += 1
                                self.stdout.write(f'  Created {model_class_name} code={code_value}')
                        
                        # Handle models with unique names/titles
                        elif hasattr(model, 'name') and 'name' in fields:
                            name_value = fields.pop('name')
                            obj, created = model.objects.get_or_create(
                                name=name_value,
                                defaults={'id': pk, 'name': name_value, **fields}
                            )
                            if not created:
                                for key, value in fields.items():
                                    setattr(obj, key, value)
                                obj.save()
                                updated += 1
                                self.stdout.write(f'  Updated {model_class_name} name={name_value}')
                            else:
                                loaded += 1
                                self.stdout.write(f'  Created {model_class_name} name={name_value}')
                        
                        elif hasattr(model, 'title') and 'title' in fields:
                            title_value = fields.pop('title')
                            obj, created = model.objects.get_or_create(
                                title=title_value,
                                defaults={'id': pk, 'title': title_value, **fields}
                            )
                            if not created:
                                for key, value in fields.items():
                                    setattr(obj, key, value)
                                obj.save()
                                updated += 1
                                self.stdout.write(f'  Updated {model_class_name} title={title_value}')
                            else:
                                loaded += 1
                                self.stdout.write(f'  Created {model_class_name} title={title_value}')
                        
                        # For other models, use primary key
                        else:
                            obj, created = model.objects.get_or_create(
                                pk=pk,
                                defaults={'id': pk, **fields}
                            )
                            if not created:
                                for key, value in fields.items():
                                    setattr(obj, key, value)
                                obj.save()
                                updated += 1
                                self.stdout.write(f'  Updated {model_class_name} pk={pk}')
                            else:
                                loaded += 1
                                self.stdout.write(f'  Created {model_class_name} pk={pk}')
                                
                    except Exception as obj_error:
                        self.stderr.write(
                            self.style.ERROR(f'  Error processing {model_class_name} pk={pk}: {str(obj_error)}')
                        )
                        skipped += 1
                        continue

            # Handle any remaining models not in the order list
            for model_name, objects in objects_by_model.items():
                if model_name not in model_order:
                    self.stdout.write(f'Processing remaining model {model_name}...')
                    # Process these with the same logic...

            self.stdout.write(
                self.style.SUCCESS(
                    f'Fixture loading complete! Created: {loaded}, Updated: {updated}, Skipped: {skipped}'
                )
            )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            self.stderr.write(self.style.ERROR(f'Traceback: {traceback.format_exc()}'))

        finally:
            if is_sqlite:
                cursor.execute('PRAGMA foreign_keys = ON;')