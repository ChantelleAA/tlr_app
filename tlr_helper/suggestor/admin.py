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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
            
            if self.instance.strand:
                # Filter substrands by strand
                self.fields['substrand'].queryset = SubStrand.objects.filter(
                    strand=self.instance.strand
                )
            
            if self.instance.substrand:
                # Filter content standards by substrand
                self.fields['standard'].queryset = ContentStandard.objects.filter(
                    substrand=self.instance.substrand
                )
            
            if self.instance.standard:
                # Filter indicators by content standard
                self.fields['indicator'].queryset = Indicator.objects.filter(
                    standard=self.instance.standard
                )

@admin.register(Tlr)
class TlrAdmin(admin.ModelAdmin):
    form = TlrAdminForm
    inlines = [TlrImageInline, TlrVideoInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'brief_description', 'tlr_type', 'intended_use', 'is_published')
        }),
        ('Curriculum Alignment', {
            'fields': (
                'class_level', 'subject', 'term', 'strand', 'substrand', 
                'standard', 'indicator'
            ),
            'description': 'Select from top to bottom - each field filters the next'
        }),
        ('Educational Context', {
            'fields': (
                'themes', 'key_learning_areas', 'competencies', 'goals'
            ),
            'classes': ('collapse',)
        }),
        ('Learning Design', {
            'fields': (
                'time_needed', 'class_size', 'bloom_level', 'learning_outcome',
                'special_needs', 'learning_styles'
            ),
            'classes': ('collapse',)
        }),
        ('Resources & Implementation', {
            'fields': (
                'materials', 'budget_band', 'resource_types', 
                'steps_to_make', 'tips_for_use'
            ),
            'classes': ('collapse',)
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
    
    # Horizontal filter for many-to-many fields
    filter_horizontal = (
        'materials', 'themes', 'key_learning_areas', 'competencies',
        'resource_types', 'goals', 'special_needs', 'learning_styles'
    )
    
    readonly_fields = ('slug', 'last_updated')
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_subjects_count', 'get_tlr_count')
    search_fields = ('name', 'code')
    
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
    
    def get_tlr_count(self, obj):
        return obj.tlr_set.count()
    get_tlr_count.short_description = 'Used in TLRs'

@admin.register(SpecialNeed)
class SpecialNeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(LearningStyle)
class LearningStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

# Register the remaining models with basic configuration
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(KeyLearningArea)
class KeyLearningAreaAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(CoreCompetency)
class CoreCompetencyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(GoalTag)
class GoalTagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

# Configure admin site headers
admin.site.site_header = "TLR Management System"
admin.site.site_title = "TLR Admin"
admin.site.index_title = "Teaching and Learning Resources Administration"