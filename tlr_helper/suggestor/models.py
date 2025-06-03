from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify

INTENDED_CHOICES = [
    ("intro", "Introduction"),
    ("aid", "Teaching Aid"),
    ("assessment", "Assessment"),
]

TIME_NEEDED_CHOICES = [
    ("starter", "Starter activity (5–10 mins)"),
    ("short", "Short activity (10–20 mins)"),
    ("core", "Main activity (20–40 mins)"),
    ("wrap", "Wrap-up / Review (5–15 mins)"),
    ("homework", "Homework / Take-home"),
    ("reusable", "Reusable or ongoing resource"),
]


CLASS_SIZE_BANDS = [
    ("small", "≤ 25"),
    ("medium", "26 – 40"),
    ("large", "41+"),
]

BLOOM_LEVELS = [
    ("remember", "Remember (recall facts, terms)"),
    ("understand", "Understand (explain ideas)"),
    ("apply", "Apply (use info in new ways)"),
    ("analyze", "Analyze (compare, contrast)"),
    ("evaluate", "Evaluate (defend opinions, judge value)"),
    ("create", "Create (develop or brain storm on idea)"),
]

BUDGET_BANDS = [
    ("none", "₵0 (No cost – use recycled or available materials)"),
    ("low", "₵1 – ₵10"),
    ("medium", "₵11 – ₵30"),
    ("high", "₵31 – ₵100"),
    ("very_high", "₵101+"),
]

SPECIAL_NEEDS_CHOICES = [
    ("none", "None"),
    ("dyslexia", "Dyslexia"),
    ("adhd", "ADHD"),
    ("visual", "Visual Impairment"),
    ("hearing", "Hearing Impairment"),
    ("autism", "Autism Spectrum"),
    ("other", "Other"),
]

TLR_TYPES = [
    ("manipulative", "Manipulative"),
    ("flashcard", "Flashcard"),
    ("poster", "Poster"),
    ("audio", "Audio"),
    ("video", "Video"),
    ("game", "Game"),
]
# ----- Supporting Models -----
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
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    # class Meta:
    #     unique_together = ("class_level", "title")
    def __str__(self):
        return f"{self.title} ({self.class_level})"

class Theme(models.Model):
    title = models.CharField(max_length=120, unique=True)
    def __str__(self):
        return self.title

class KeyLearningArea(models.Model):
    title = models.CharField(max_length=120, unique=True)
    def __str__(self):
        return self.title

class CoreCompetency(models.Model):
    title = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return self.title

class ResourceType(models.Model):
    title = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return self.title

class GoalTag(models.Model):
    title = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return self.title

class SpecialNeed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class LearningStyle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# ----- Curriculum Structure -----
class Strand(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True, related_name='strands')
    term = models.PositiveSmallIntegerField(choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")])
    title = models.CharField(max_length=120)
    themes = models.ManyToManyField(Theme, blank=True)
    key_learning_areas = models.ManyToManyField(KeyLearningArea, blank=True)
    competencies = models.ManyToManyField(CoreCompetency, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_level} – {self.title}"

class SubStrand(models.Model):
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, related_name='substrands')
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ContentStandard(models.Model):
    substrand = models.ForeignKey(SubStrand, on_delete=models.CASCADE, related_name='standards')
    code = models.CharField(max_length=20)
    description = models.TextField()
    competencies = models.ManyToManyField(CoreCompetency, blank=True)
    goals = models.ManyToManyField(GoalTag, blank=True)
    class Meta:
        unique_together = ("substrand", "code")
    def __str__(self):
        return self.code

class Indicator(models.Model):
    standard = models.ForeignKey(ContentStandard, on_delete=models.CASCADE, related_name='indicators')
    code = models.CharField(max_length=20)
    description = models.TextField()
    competencies = models.ManyToManyField(CoreCompetency, blank=True)
    goals = models.ManyToManyField(GoalTag, blank=True)
    class Meta:
        unique_together = ("standard", "code")
    def __str__(self):
        return self.code
    
class TlrImage(models.Model):
    tlr = models.ForeignKey("Tlr", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tlr_images/")
    caption = models.CharField(max_length=200, blank=True)

class TlrVideo(models.Model):
    tlr = models.ForeignKey("Tlr", related_name="videos", on_delete=models.CASCADE)
    url = models.URLField()
    caption = models.CharField(max_length=200, blank=True)


# ----- Main TLR -----
class Tlr(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    subject = ChainedForeignKey(
        Subject,
        chained_field="class_level",
        chained_model_field="class_level",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    term = models.PositiveSmallIntegerField(null=True, blank=True)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, null=True, blank=True)
    substrand = models.ForeignKey(SubStrand, on_delete=models.CASCADE, null=True, blank=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=True, blank=True)
    standard = models.ForeignKey(ContentStandard, on_delete=models.CASCADE, null=True, blank=True)

    themes = models.ManyToManyField(Theme, blank=True)
    key_learning_areas = models.ManyToManyField(KeyLearningArea, blank=True)
    competencies = models.ManyToManyField(CoreCompetency, blank=True)
    resource_types = models.ManyToManyField(ResourceType, blank=True)
    goals = models.ManyToManyField(GoalTag, blank=True)

    title = models.CharField(max_length=120)
    brief_description = models.TextField()
    materials = models.ManyToManyField(Material, blank=True)
    time_needed = models.CharField(max_length=10, choices=TIME_NEEDED_CHOICES, default="lesson")
    steps_to_make = models.TextField(blank=True)
    tips_for_use = models.TextField(blank=True)
    intended_use = models.CharField(max_length=20, choices=INTENDED_CHOICES, blank=True, null=True)
    tlr_type = models.CharField(max_length=20, choices=TLR_TYPES, blank=True, null=True)
    special_needs = models.ManyToManyField(SpecialNeed, blank=True)
    learning_styles = models.ManyToManyField(LearningStyle, blank=True)
    class_size = models.CharField(max_length=10, choices=CLASS_SIZE_BANDS, blank=True, null=True)
    bloom_level = models.CharField(max_length=20, choices=BLOOM_LEVELS, blank=True, null=True)
    budget_band = models.CharField(max_length=20, choices=BUDGET_BANDS, blank=True, null=True)
    learning_outcome = models.TextField(blank=True)
    # image = models.ImageField(upload_to="tlr_images/", null=True, blank=True)
    # video_url = models.URLField(null=True, blank=True)

    search_keywords = models.TextField(blank=True)
    slug = models.SlugField(blank=True, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.indicator:
            self.standard = self.indicator.standard
            self.substrand = self.standard.substrand
            self.strand = self.substrand.strand
            self.subject = self.strand.subject
            self.class_level = self.strand.class_level
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# @receiver(post_migrate)
def populate_initial_data(sender, **kwargs):
    if sender.label != "suggestor":
        return

    # Import models dynamically
    ClassLevel = apps.get_model("suggestor", "ClassLevel")
    Subject = apps.get_model("suggestor", "Subject")
    Theme = apps.get_model("suggestor", "Theme")
    KeyLearningArea = apps.get_model("suggestor", "KeyLearningArea")
    CoreCompetency = apps.get_model("suggestor", "CoreCompetency")
    GoalTag = apps.get_model("suggestor", "GoalTag")
    ResourceType = apps.get_model("suggestor", "ResourceType")
    SpecialNeed = apps.get_model("suggestor", "SpecialNeed")
    LearningStyle = apps.get_model("suggestor", "LearningStyle")

    if ClassLevel.objects.exists():
        print("Initial data already exists. Skipping post_migrate data creation.")
        return

    print("Creating initial data via post_migrate signal...")



    # Subjects by Class
    SUBJECTS_BY_CLASS = {
        "Creche": ["Language and Literacy", "Numeracy", "Creative Arts", "Environmental Studies", "Physical Development", "Music and Movement"],
        "Nursery": ["Language and Literacy", "Numeracy", "Creative Arts", "Environmental Studies", "Physical Development", "Music and Movement"],
        "KG1": ["Language and Literacy", "Numeracy", "Our World Our People", "Creative Arts", "Physical Development", "Religious and Moral Education"],
        "KG2": ["Language and Literacy", "Numeracy", "Our World Our People", "Creative Arts", "Physical Development", "Religious and Moral Education"],
        "Class 1": ["English Language", "Ghanaian Language", "Mathematics", "Science", "Our World Our People", "Creative Arts", "Physical Education", "Religious and Moral Education", "Computing"],
        "Class 2": ["English Language", "Ghanaian Language", "Mathematics", "Science", "Our World Our People", "Creative Arts", "Physical Education", "Religious and Moral Education", "Computing"],
        "Class 3": ["English Language", "Ghanaian Language", "Mathematics", "Science", "Our World Our People", "Creative Arts", "Physical Education", "Religious and Moral Education", "Computing"]
    }

    # Class levels
    for i, name in enumerate(SUBJECTS_BY_CLASS.keys(), start=1):
        ClassLevel.objects.get_or_create(code=str(i), name=name)

    # Subjects per class level
    for cl_name, subj_list in SUBJECTS_BY_CLASS.items():
        try:
            cl = ClassLevel.objects.get(name=cl_name)
        except ClassLevel.DoesNotExist:
            continue
        for title in subj_list:
            Subject.objects.get_or_create(class_level=cl, title=title)

    # Themes
    themes = ["Myself", "My Environment", "My Community", "My Nation", "Our Values"]
    for t in themes:
        Theme.objects.get_or_create(title=t)

    # Key Learning Areas
    kla = ["Literacy", "Numeracy", "PSED", "Science and Environment", "Creative Arts", "Religious and Moral", "Computing"]
    for k in kla:
        KeyLearningArea.objects.get_or_create(title=k)

    # Core Competencies
    comps = ["Critical Thinking", "Creativity", "Communication", "Collaboration", "Personal Development", "Digital Literacy"]
    for c in comps:
        CoreCompetency.objects.get_or_create(title=c)

    # Goal Tags
    for g in ["Introduce", "Reinforce", "Assess"]:
        GoalTag.objects.get_or_create(title=g)

    # Resource Types
    for r in ["Poster", "Flashcards", "Manipulatives", "Charts", "Storybooks", "Games"]:
        ResourceType.objects.get_or_create(title=r)

    # Special Needs
    needs = [
        ("Dyslexia", "Difficulty reading and decoding words"),
        ("ADHD", "Attention deficit, trouble focusing"),
        ("Visual Impairment", "Low vision or blindness"),
        ("Hearing Impairment", "Partial or full hearing loss"),
        ("Autism Spectrum", "Neurodiverse needs related to interaction and focus"),
        ("Other", "Any other learning need not listed")
    ]
    for name, desc in needs:
        SpecialNeed.objects.get_or_create(name=name, defaults={"description": desc})

    # Learning Styles
    styles = [
        ("Visual", "Prefers diagrams, images, charts"),
        ("Auditory", "Learns better through listening"),
        ("Kinesthetic", "Prefers hands-on activities"),
        ("Read/Write", "Learns best through reading and writing"),
        ("Multimodal", "Uses a combination of learning styles")
    ]
    for name, desc in styles:
        LearningStyle.objects.get_or_create(name=name, defaults={"description": desc})