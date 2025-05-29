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

# choose whatever labels make sense to you
CLASS_SIZE_BANDS = [
    ("small", "≤ 25"),
    ("medium", "26 – 40"),
    ("large", "41+"),
]

BLOOM_LEVELS = [
    ("remember", "Remember"),
    ("understand", "Understand"),
    ("apply", "Apply"),
    ("analyse", "Analyse"),
    ("evaluate", "Evaluate"),
    ("create", "Create"),
]

BUDGET_BANDS = [
    ("low", "₵0 – 5"),
    ("mid", "₵6 – 20"),
    ("high", "₵21 +"),
]


class Material(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

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

class Theme(models.Model):
    """KG / lower-primary integrated themes."""
    title = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.title


class KeyLearningArea(models.Model):
    """Numeracy, Literacy, PSED, etc."""
    title = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.title


class CoreCompetency(models.Model):
    """Critical Thinking, Creativity …"""
    title = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.title


class ResourceType(models.Model):
    """Poster, Game, Manipulative …"""
    title = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.title


class GoalTag(models.Model):
    """Quick goal-based route (Introduce / Reinforce / Assess / Engage)."""
    title = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.title

class Subject(models.Model):
    """Core Learning Area / School subject (Maths, English, etc.)."""
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)

    class Meta:
        unique_together = ("class_level", "title")

    def __str__(self):
        return f"{self.title} ({self.class_level})"


class ContentStandard(models.Model):
    """Optional: if you want to keep the full SBC hierarchy."""
    substrand = models.ForeignKey(SubStrand, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        unique_together = ("substrand", "code")

    def __str__(self):
        return self.code


class Indicator(models.Model):
    standard = models.ForeignKey(ContentStandard, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        unique_together = ("standard", "code")

    def __str__(self):
        return self.code

class Tlr(models.Model):
    # --- curriculum tags ---
    class_level   = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    term          = models.PositiveSmallIntegerField(null=True, blank=True)  # 1-3
    strand        = models.ForeignKey(Strand, on_delete=models.CASCADE, null=True, blank=True)
    substrand     = models.ForeignKey(SubStrand, on_delete=models.CASCADE, null=True, blank=True)
    indicator     = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True, blank=True)

    # --- alternate tags ---
    themes            = models.ManyToManyField(Theme, blank=True)
    key_learning_areas = models.ManyToManyField(KeyLearningArea, blank=True)
    competencies      = models.ManyToManyField(CoreCompetency, blank=True)
    resource_types    = models.ManyToManyField(ResourceType, blank=True)
    goals             = models.ManyToManyField(GoalTag, blank=True)

    # --- existing fields ---
    title = models.CharField(max_length=120)
    brief_description = models.TextField()
    materials         = models.ManyToManyField(Material, blank=True)
    time_needed       = models.CharField(max_length=10, choices=TIME_CHOICES, default="lesson")
    steps_to_make   = models.TextField(blank=True)  
    tips_for_use    = models.TextField(blank=True) 
    intended_use = models.CharField(max_length=20, choices=INTENDED_CHOICES, blank=True, null=True)
    tlr_type = models.CharField(max_length=20, blank=True, null=True) 



    def __str__(self):
        return self.title
