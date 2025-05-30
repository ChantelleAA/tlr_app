from django.contrib import admin
from .models import (
    Tlr, ClassLevel, Strand, SubStrand, Material, Theme,
    KeyLearningArea, CoreCompetency, ResourceType, GoalTag,
    Subject, ContentStandard, Indicator
)

@admin.register(Tlr)
class TlrAdmin(admin.ModelAdmin):
    list_display = ("title", "strand", "class_level", "intended_use")
    search_fields = ("title", "strand", "sub_strand")
    list_filter = ("class_level", "intended_use", "tlr_type", "materials")

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    search_fields = ("name",)

admin.site.register(ClassLevel)
admin.site.register(Strand)
admin.site.register(SubStrand)
admin.site.register(Theme)
admin.site.register(KeyLearningArea)
admin.site.register(CoreCompetency)
admin.site.register(ResourceType)
admin.site.register(GoalTag)
admin.site.register(Subject)
admin.site.register(ContentStandard)
admin.site.register(Indicator)
