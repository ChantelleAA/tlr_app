from django.contrib import admin
from .models import Tlr, Material


@admin.register(Tlr)
class TlrAdmin(admin.ModelAdmin):
    list_display = ("title", "strand", "class_level", "intended_use")
    search_fields = ("title", "strand", "sub_strand")
    list_filter = ("class_level", "intended_use", "tlr_type", "materials")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    search_fields = ("name",)
