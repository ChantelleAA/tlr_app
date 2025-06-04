from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

INTENDED_CHOICES = [
    ("intro", "Introduction"),
    ("aid", "Teaching Aid"),
    ("assessment", "Assessment"),
]

SUBJECTS_BY_CLASS = {
    "Crèche": [
        "Language and Literacy",
        "Numeracy",
        "Creative Arts",
        "Environmental Studies",
        "Physical Development",
        "Music and Movement"
    ],
    "Nursery": [
        "Language and Literacy",
        "Numeracy",
        "Creative Arts",
        "Environmental Studies",
        "Physical Development",
        "Music and Movement"
    ],
    "KG1": [
        "Language and Literacy",
        "Numeracy",
        "Our World Our People",
        "Creative Arts",
        "Physical Development",
        "Religious and Moral Education"
    ],
    "KG2": [
        "Language and Literacy",
        "Numeracy",
        "Our World Our People",
        "Creative Arts",
        "Physical Development",
        "Religious and Moral Education"
    ],
    "Class 1": [
        "English Language",
        "Ghanaian Language",
        "Mathematics",
        "Science",
        "Our World Our People",
        "Creative Arts",
        "Physical Education",
        "Religious and Moral Education",
        "Computing"
    ],
    "Class 2": [
        "English Language",
        "Ghanaian Language",
        "Mathematics",
        "Science",
        "Our World Our People",
        "Creative Arts",
        "Physical Education",
        "Religious and Moral Education",
        "Computing"
    ],
    "Class 3": [
        "English Language",
        "Ghanaian Language",
        "Mathematics",
        "Science",
        "Our World Our People",
        "Creative Arts",
        "Physical Education",
        "Religious and Moral Education",
        "Computing"
    ],
}


classes = ["Crèche", "Nursery", "KG1", "KG2", "Class 1", "Class 2", "Class 3"]
CLASS_CHOICES = [(i, i) if " " not in i else (i, i[-1]) for i in classes]

TIME_CHOICES = [
    ("quick", "5-10 min"),
    ("lesson", "30-40 min"),
    ("reusable", "Reusable / multi-use"),
]

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
    ("low", "₵0 – 50"),
    ("lower-mid", "₵50 – 100"),
    ("high", "₵100 +"),
]

LEARNING_DIFFICULTY_CHOICES = [
    ("none", "None"),
    ("dyslexia", "Dyslexia"),
    ("adhd", "ADHD"),
    ("visual", "Visual Impairment"),
    ("hearing", "Hearing Impairment"),
    ("autism", "Autism Spectrum"),
    ("other", "Other"),
]

class Material(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

class ClassLevel(models.Model):
    code = models.CharField(max_length=5, unique=True) 
    name = models.CharField(max_length=20)               
    def __str__(self):
        return self.name

class Subject(models.Model):
    """Core Learning Area / School subject (Maths, English, etc.)."""
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)

    class Meta:
        unique_together = ("class_level", "title")

    def __str__(self):
        return f"{self.title} ({self.class_level})"

class Strand(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True) 
    term = models.PositiveSmallIntegerField(choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")])
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
    class_level   = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    # subject       = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    subject = ChainedForeignKey(
    Subject,
    chained_field="class_level",
    chained_model_field="class_level",
    show_all=False,
    auto_choose=True,
    sort=True,
    null=True,
    blank=True,
    on_delete=models.CASCADE)
    term          = models.PositiveSmallIntegerField(null=True, blank=True)
    strand        = models.ForeignKey(Strand, on_delete=models.CASCADE, null=True, blank=True)
    substrand     = models.ForeignKey(SubStrand, on_delete=models.CASCADE, null=True, blank=True)
    indicator     = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True, blank=True)

    themes            = models.ManyToManyField(Theme, blank=True)
    key_learning_areas = models.ManyToManyField(KeyLearningArea, blank=True)
    competencies      = models.ManyToManyField(CoreCompetency, blank=True)
    resource_types    = models.ManyToManyField(ResourceType, blank=True)
    goals             = models.ManyToManyField(GoalTag, blank=True)

    title = models.CharField(max_length=120)
    brief_description = models.TextField()
    materials         = models.ManyToManyField(Material, blank=True)
    time_needed       = models.CharField(max_length=10, choices=TIME_CHOICES, default="lesson")
    steps_to_make   = models.TextField(blank=True)  
    tips_for_use    = models.TextField(blank=True) 
    intended_use = models.CharField(max_length=20, choices=INTENDED_CHOICES, blank=True, null=True)
    tlr_type = models.CharField(max_length=20, blank=True, null=True) 
    learning_difficulty = models.CharField(
        max_length=20,
        choices=LEARNING_DIFFICULTY_CHOICES,
        default="none",
        blank=True,
        null=True,
    )


    def __str__(self):
        return self.title


@receiver(post_migrate)
def _populate_subjects(sender, **kwargs):
    """
    After every migrate, be sure each Subject in SUBJECTS_BY_CLASS
    exists for its ClassLevel (just like ClassLevels were pre-loaded
    from the `classes` list).
    """
    if sender.label != "suggestor":          # ← your app label
        return

    ClassLevel = apps.get_model("suggestor", "ClassLevel")
    Subject     = apps.get_model("suggestor", "Subject")

    for cls_name, subj_titles in SUBJECTS_BY_CLASS.items():
        try:
            cl = ClassLevel.objects.get(name=cls_name)
        except ClassLevel.DoesNotExist:
            continue                         # class not in DB yet

        for title in subj_titles:
            Subject.objects.get_or_create(class_level=cl, title=title)