# management/commands/load_fixtures_safe.py

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection, transaction
from django.apps import apps
import json

class Command(BaseCommand):
    help = 'Safely loads initial_data.json with proper foreign key handling'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        db_engine = settings.DATABASES['default']['ENGINE']
        is_sqlite = 'sqlite' in db_engine

        try:
            if is_sqlite:
                cursor.execute('PRAGMA foreign_keys = OFF;')

            self.stdout.write('Loading initial_data.json...')

            # Load fixture data
            with open('suggestor/fixtures/initial_data.json', 'r') as f:
                fixture_data = json.load(f)

            created_count = 0
            updated_count = 0
            skipped_count = 0

            # Process models in dependency order to handle foreign keys properly
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
                'suggestor.subject',           # Depends on ClassLevel
                'suggestor.strand',            # Depends on ClassLevel, Subject
                'suggestor.substrand',         # Depends on Strand
                'suggestor.contentstandard',   # Depends on SubStrand
                'suggestor.indicator',         # Depends on ContentStandard
                'suggestor.tlr',              # Depends on all above
                'suggestor.tlrimage',         # Depends on TLR
                'suggestor.tlrvideo',         # Depends on TLR
            ]

            # Group fixture data by model
            objects_by_model = {}
            for obj_data in fixture_data:
                model_name = obj_data['model']
                if model_name not in objects_by_model:
                    objects_by_model[model_name] = []
                objects_by_model[model_name].append(obj_data)

            # Process each model in order
            for model_name in model_order:
                if model_name not in objects_by_model:
                    continue
                    
                self.stdout.write(f'Processing {model_name}...')
                
                for obj_data in objects_by_model[model_name]:
                    try:
                        app_label, model_class_name = model_name.split('.')
                        model_class = apps.get_model(app_label, model_class_name)
                        
                        pk = obj_data['pk']
                        fields = obj_data['fields'].copy()
                        
                        # Resolve foreign key relationships
                        resolved_fields = self.resolve_foreign_keys(model_class, fields)
                        
                        # Handle models with unique identifiers
                        if self.has_unique_field(model_class, 'code') and 'code' in resolved_fields:
                            code_value = resolved_fields['code']
                            obj, created = model_class.objects.update_or_create(
                                code=code_value,
                                defaults=resolved_fields
                            )
                            action = "Created" if created else "Updated"
                            self.stdout.write(f'  {action} {model_class_name.lower()} code={code_value}')
                            
                        elif self.has_unique_field(model_class, 'name') and 'name' in resolved_fields:
                            name_value = resolved_fields['name']
                            obj, created = model_class.objects.update_or_create(
                                name=name_value,
                                defaults=resolved_fields
                            )
                            action = "Created" if created else "Updated"
                            self.stdout.write(f'  {action} {model_class_name.lower()} name={name_value}')
                            
                        elif self.has_unique_field(model_class, 'title') and 'title' in resolved_fields:
                            title_value = resolved_fields['title']
                            obj, created = model_class.objects.update_or_create(
                                title=title_value,
                                defaults=resolved_fields
                            )
                            action = "Created" if created else "Updated"
                            self.stdout.write(f'  {action} {model_class_name.lower()} title={title_value}')
                            
                        else:
                            # For models without unique fields, use primary key
                            obj, created = model_class.objects.update_or_create(
                                pk=pk,
                                defaults=resolved_fields
                            )
                            action = "Created" if created else "Updated"
                            self.stdout.write(f'  {action} {model_class_name.lower()} pk={pk}')
                            
                        # Handle many-to-many fields
                        self.handle_many_to_many(obj, obj_data['fields'], model_class)
                        
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                            
                    except Exception as e:
                        self.stdout.write(f'  Error processing {model_class_name.lower()} pk={pk}: {str(e)}')
                        skipped_count += 1
                        continue

            self.stdout.write(
                self.style.SUCCESS(
                    f'Fixture loading complete! Created: {created_count}, Updated: {updated_count}, Skipped: {skipped_count}'
                )
            )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            self.stderr.write(self.style.ERROR(f'Traceback: {traceback.format_exc()}'))

        finally:
            if is_sqlite:
                cursor.execute('PRAGMA foreign_keys = ON;')

    def resolve_foreign_keys(self, model_class, fields):
        """Convert foreign key IDs to actual model instances"""
        resolved_fields = {}
        
        for field_name, value in fields.items():
            try:
                field = model_class._meta.get_field(field_name)
                
                # Skip many-to-many fields (handle separately)
                if field.many_to_many:
                    continue
                    
                # Handle foreign key fields
                if hasattr(field, 'related_model') and field.related_model:
                    if value is not None:
                        try:
                            # Convert ID to actual model instance
                            related_obj = field.related_model.objects.get(pk=value)
                            resolved_fields[field_name] = related_obj
                        except field.related_model.DoesNotExist:
                            self.stdout.write(f'    Warning: Related {field.related_model.__name__} with pk={value} not found for field {field_name}')
                            # Skip this field if related object doesn't exist
                            continue
                        except field.related_model.MultipleObjectsReturned:
                            # Handle multiple objects returned
                            related_obj = field.related_model.objects.filter(pk=value).first()
                            resolved_fields[field_name] = related_obj
                    else:
                        resolved_fields[field_name] = None
                else:
                    # Regular field, keep as is
                    resolved_fields[field_name] = value
                    
            except Exception:
                # If field doesn't exist or other error, keep original value
                resolved_fields[field_name] = value
                
        return resolved_fields

    def handle_many_to_many(self, obj, original_fields, model_class):
        """Handle many-to-many field assignments after object creation"""
        for field_name, value in original_fields.items():
            try:
                field = model_class._meta.get_field(field_name)
                
                if field.many_to_many and value:
                    # Get the related manager
                    manager = getattr(obj, field_name)
                    
                    # Clear existing relationships
                    manager.clear()
                    
                    # Add new relationships
                    for pk_value in value:
                        try:
                            related_obj = field.related_model.objects.get(pk=pk_value)
                            manager.add(related_obj)
                        except field.related_model.DoesNotExist:
                            self.stdout.write(f'    Warning: Related {field.related_model.__name__} with pk={pk_value} not found for M2M field {field_name}')
                            continue
                            
            except Exception:
                # Skip if field doesn't exist or other error
                continue

    def has_unique_field(self, model_class, field_name):
        """Check if model has a unique field with given name"""
        try:
            field = model_class._meta.get_field(field_name)
            return field.unique
        except:
            return False