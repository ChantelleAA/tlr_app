from django.contrib import admin
from django import forms
from django.db import models
from .models import (
    Tlr, ClassLevel, Strand, SubStrand, Material, Theme,
    KeyLearningArea, CoreCompetency, ResourceType, GoalTag,
    Subject, ContentStandard, Indicator, TlrImage, TlrVideo,
    SpecialNeed, LearningStyle
)

class TlrImageInline(admin.TabularInline):
    model = TlrImage
    extra = 1
    fields = ('image', 'caption')

class TlrVideoInline(admin.TabularInline):
    model = TlrVideo
    extra = 1
    fields = ('url', 'caption')

# Custom form for cascading relationships
class TlrAdminForm(forms.ModelForm):
    class Meta:
        model = Tlr
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Convert empty strings to None for foreign key fields
        foreign_key_fields = [
            'class_level', 'subject', 'strand', 'substrand', 
            'standard', 'indicator', 'created_by'
        ]
        
        for field_name in foreign_key_fields:
            if field_name in cleaned_data:
                if cleaned_data[field_name] == '' or cleaned_data[field_name] == 'None':
                    cleaned_data[field_name] = None
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set empty labels for better UX
        self.fields['subject'].empty_label = "Select class level first..."
        self.fields['strand'].empty_label = "Select subject first..."
        self.fields['substrand'].empty_label = "Select strand first..."
        self.fields['standard'].empty_label = "Select substrand first..."
        self.fields['indicator'].empty_label = "Select standard first..."
        
        # If editing existing TLR, filter related fields based on selections
        if self.instance.pk:
            if self.instance.class_level:
                # Filter subjects by class level
                self.fields['subject'].queryset = Subject.objects.filter(
                    class_level=self.instance.class_level
                )
                # Filter strands by class level
                self.fields['strand'].queryset = Strand.objects.filter(
                    class_level=self.instance.class_level
                )
            else:
                self.fields['subject'].queryset = Subject.objects.none()
                self.fields['strand'].queryset = Strand.objects.none()
            
            if self.instance.strand:
                # Filter substrands by strand
                self.fields['substrand'].queryset = SubStrand.objects.filter(
                    strand=self.instance.strand
                )
            else:
                self.fields['substrand'].queryset = SubStrand.objects.none()
            
            if self.instance.substrand:
                # Filter content standards by substrand
                self.fields['standard'].queryset = ContentStandard.objects.filter(
                    substrand=self.instance.substrand
                )
            else:
                self.fields['standard'].queryset = ContentStandard.objects.none()
            
            if self.instance.standard:
                # Filter indicators by content standard
                self.fields['indicator'].queryset = Indicator.objects.filter(
                    standard=self.instance.standard
                )
            else:
                self.fields['indicator'].queryset = Indicator.objects.none()
        else:
            # For new records, start with empty querysets except class_level
            self.fields['subject'].queryset = Subject.objects.none()
            self.fields['strand'].queryset = Strand.objects.none()
            self.fields['substrand'].queryset = SubStrand.objects.none()
            self.fields['standard'].queryset = ContentStandard.objects.none()
            self.fields['indicator'].queryset = Indicator.objects.none()

@admin.register(Tlr)
class TlrAdmin(admin.ModelAdmin):
    form = TlrAdminForm
    inlines = [TlrImageInline, TlrVideoInline]
    
    # Enable autocomplete and popup add/edit/delete buttons
    autocomplete_fields = ['class_level', 'subject', 'strand', 'substrand', 'standard', 'indicator']
    raw_id_fields = ['created_by']  # For user selection with popup
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'brief_description', 'tlr_type', 'intended_use', 'is_published')
        }),
        ('Curriculum Alignment', {
            'fields': (
                'class_level', 'subject', 'term', 'strand', 'substrand', 
                'standard', 'indicator'
            ),
            'description': 'Select from top to bottom - each field filters the next. Use the green + buttons to add new items.'
        }),
        ('Educational Context', {
            'fields': (
                'themes', 'key_learning_areas', 'competencies', 'goals'
            ),
            'classes': ('collapse',),
            'description': 'Use the green + buttons to add new themes, learning areas, competencies, or goals.'
        }),
        ('Learning Design', {
            'fields': (
                'time_needed', 'class_size', 'bloom_level', 'learning_outcome',
                'special_needs', 'learning_styles'
            ),
            'classes': ('collapse',),
            'description': 'Use the green + buttons to add new special needs or learning styles.'
        }),
        ('Resources & Implementation', {
            'fields': (
                'materials', 'budget_band', 'resource_types', 
                'steps_to_make', 'tips_for_use'
            ),
            'classes': ('collapse',),
            'description': 'Use the green + buttons to add new materials or resource types.'
        }),
        ('Metadata', {
            'fields': ('search_keywords', 'created_by', 'download_count'),
            'classes': ('collapse',)
        })
    )
    
    list_display = (
        'title', 'class_level', 'subject', 'strand', 'tlr_type', 
        'intended_use', 'is_published', 'download_count'
    )
    
    list_filter = (
        'class_level', 'subject', 'intended_use', 'tlr_type', 
        'time_needed', 'is_published', 'bloom_level'
    )
    
    search_fields = (
        'title', 'brief_description', 'search_keywords',
        'strand__title', 'substrand__title'
    )
    
    # Horizontal filter for many-to-many fields with add/change/delete buttons
    filter_horizontal = (
        'materials', 'themes', 'key_learning_areas', 'competencies',
        'resource_types', 'goals', 'special_needs', 'learning_styles'
    )
    
    readonly_fields = ('slug', 'last_updated')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Override form field widgets to handle empty strings better
        for field_name in ['class_level', 'subject', 'strand', 'substrand', 'standard', 'indicator']:
            if field_name in form.base_fields:
                field = form.base_fields[field_name]
                if hasattr(field, 'queryset'):
                    field.empty_label = "Select..."
                    field.required = False
        
        return form

    def get_object(self, request, object_id, from_field=None):
        """Override to handle cases where foreign keys might be empty strings"""
        try:
            obj = super().get_object(request, object_id, from_field)
            if obj:
                # Clean up any empty string foreign keys
                foreign_key_fields = ['class_level', 'subject', 'strand', 'substrand', 'standard', 'indicator', 'created_by']
                changed = False
                for field_name in foreign_key_fields:
                    field_id_name = f"{field_name}_id"
                    field_value = getattr(obj, field_id_name, None)
                    if field_value == '':
                        setattr(obj, field_id_name, None)
                        changed = True
                
                # Save if we made changes to clean up the data
                if changed:
                    obj.save(update_fields=[f"{f}_id" for f in foreign_key_fields])
            
            return obj
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in TlrAdmin.get_object for ID {object_id}: {e}")
            raise
    
    def save_model(self, request, obj, form, change):
        # Clean empty strings before saving
        foreign_key_fields = ['class_level', 'subject', 'strand', 'substrand', 'standard', 'indicator']
        
        for field_name in foreign_key_fields:
            field_value = getattr(obj, field_name, None)
            if field_value == '':
                setattr(obj, field_name, None)
        
        if not obj.created_by:
            obj.created_by = request.user
        
        super().save_model(request, obj, form, change)

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_subjects_count', 'get_tlr_count')
    search_fields = ('name', 'code')
    ordering = ('code',)
    
    def get_subjects_count(self, obj):
        return obj.subject_set.count()
    get_subjects_count.short_description = 'Subjects'
    
    def get_tlr_count(self, obj):
        return obj.tlr_set.count()
    get_tlr_count.short_description = 'TLRs'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_level', 'get_strands_count')
    list_filter = ('class_level',)
    search_fields = ('title',)
    ordering = ('class_level', 'title')
    
    def get_strands_count(self, obj):
        return obj.strands.count()
    get_strands_count.short_description = 'Strands'

@admin.register(Strand)
class StrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_level', 'subject', 'term', 'get_substrands_count')
    list_filter = ('class_level', 'subject', 'term')
    search_fields = ('title',)
    filter_horizontal = ('themes', 'key_learning_areas', 'competencies')
    readonly_fields = ('slug',)
    ordering = ('class_level', 'subject', 'term', 'title')
    
    fieldsets = (
        (None, {
            'fields': ('class_level', 'subject', 'term', 'title')
        }),
        ('Learning Elements', {
            'fields': ('themes', 'key_learning_areas', 'competencies'),
            'classes': ('collapse',)
        })
    )
    
    def get_substrands_count(self, obj):
        return obj.substrands.count()
    get_substrands_count.short_description = 'Sub-strands'

@admin.register(SubStrand)
class SubStrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'strand', 'get_strand_class_level', 'get_standards_count')
    list_filter = ('strand__class_level', 'strand__subject')
    search_fields = ('title', 'strand__title')
    readonly_fields = ('slug',)
    ordering = ('strand__class_level', 'strand__subject', 'strand__term', 'title')
    
    def get_strand_class_level(self, obj):
        return obj.strand.class_level
    get_strand_class_level.short_description = 'Class Level'
    
    def get_standards_count(self, obj):
        return obj.standards.count()
    get_standards_count.short_description = 'Standards'

@admin.register(ContentStandard)
class ContentStandardAdmin(admin.ModelAdmin):
    list_display = ('code', 'substrand', 'get_class_level', 'get_indicators_count')
    list_filter = ('substrand__strand__class_level', 'substrand__strand__subject')
    search_fields = ('code', 'description', 'substrand__title')
    filter_horizontal = ('competencies', 'goals')
    ordering = ('substrand__strand__class_level', 'substrand__strand__subject', 'code')
    
    fieldsets = (
        (None, {
            'fields': ('substrand', 'code', 'description')
        }),
        ('Learning Elements', {
            'fields': ('competencies', 'goals'),
            'classes': ('collapse',)
        })
    )
    
    def get_class_level(self, obj):
        return obj.substrand.strand.class_level
    get_class_level.short_description = 'Class Level'
    
    def get_indicators_count(self, obj):
        return obj.indicators.count()
    get_indicators_count.short_description = 'Indicators'

@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('code', 'standard', 'get_substrand', 'get_class_level')
    list_filter = (
        'standard__substrand__strand__class_level',
        'standard__substrand__strand__subject'
    )
    search_fields = ('code', 'description', 'standard__code')
    filter_horizontal = ('competencies', 'goals')
    ordering = ('standard__substrand__strand__class_level', 'standard__code', 'code')
    
    fieldsets = (
        (None, {
            'fields': ('standard', 'code', 'description')
        }),
        ('Learning Elements', {
            'fields': ('competencies', 'goals'),
            'classes': ('collapse',)
        })
    )
    
    def get_substrand(self, obj):
        return obj.standard.substrand
    get_substrand.short_description = 'Sub-strand'
    
    def get_class_level(self, obj):
        return obj.standard.substrand.strand.class_level
    get_class_level.short_description = 'Class Level'

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_tlr_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def get_tlr_count(self, obj):
        return obj.tlr_set.count()
    get_tlr_count.short_description = 'Used in TLRs'

@admin.register(SpecialNeed)
class SpecialNeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(LearningStyle)
class LearningStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

# Register the remaining models with enhanced configuration
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(KeyLearningArea)
class KeyLearningAreaAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(CoreCompetency)
class CoreCompetencyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(GoalTag)
class GoalTagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)

# Configure admin site headers
admin.site.site_header = "TLR Management System"
admin.site.site_title = "TLR Admin"
admin.site.index_title = "Teaching and Learning Resources Administration"