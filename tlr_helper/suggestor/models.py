from django.db import models

INTENDED_CHOICES = [
    ("intro", "Introduction"),
    ("aid", "Teaching Aid"),
    ("assessment", "Assessment"),
]

CLASS_CHOICES = [("KG", "KG")] + [(str(i), f"Class {i}") for i in range(1, 4)]

TIME_CHOICES = [
    ("quick", "5-10 min"),
    ("lesson", "30-40 min"),
    ("reusable", "Reusable / multi-use"),
]

class Material(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Tlr(models.Model):
    strand = models.CharField(max_length=120)
    sub_strand = models.CharField(max_length=120, blank=True)
    class_level = models.CharField(max_length=3, choices=CLASS_CHOICES)
    intended_use = models.CharField(max_length=12, choices=INTENDED_CHOICES)
    tlr_type = models.CharField(max_length=60, blank=True)           # poster, puzzle …
    title = models.CharField(max_length=120)
    brief_description = models.TextField()
    materials = models.ManyToManyField(Material, blank=True)
    time_needed = models.CharField(max_length=10, choices=TIME_CHOICES, default="lesson")
    accessibility_notes = models.TextField(blank=True)
    classroom_setup = models.CharField(max_length=120, blank=True)
    steps_to_make = models.TextField()
    tips_for_use = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
# suggestor/models.py
class ClassLevel(models.Model):
    code = models.CharField(max_length=5, unique=True)   # KG, 1, 2, 3
    name = models.CharField(max_length=20)               # “KG”, “Class 1”

    def __str__(self):
        return self.name


class Strand(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.class_level} – {self.title}"


class SubStrand(models.Model):
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

