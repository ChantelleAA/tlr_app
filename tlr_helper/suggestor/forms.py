# suggestor/forms.py
from django import forms
from .models import (
    # curriculum hierarchy
    ClassLevel, Subject, Strand, SubStrand,
    # optional tags
    Theme, KeyLearningArea, CoreCompetency, ResourceType, GoalTag, ContentStandard, Indicator, SpecialNeed, LearningStyle,
    # supporting tables
    Material,
    # constants
    INTENDED_CHOICES, TIME_NEEDED_CHOICES,
    CLASS_SIZE_BANDS, BLOOM_LEVELS, BUDGET_BANDS,
    SPECIAL_NEEDS_CHOICES,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


ROUTES = [
    ("curriculum", "By Strand / Sub-strand"),
    ("key_area",   "By Key Learning Area"),
    ("competency", "By Core Competency"),
    ("theme",      "By Theme"),
    ("resource",   "By Resource Type"),
    ("goal",       "By Quick Goal"),
]


class RouteSelectForm(forms.Form):
    route = forms.ChoiceField(
        choices=ROUTES,
        widget=forms.RadioSelect,
        label="How would you like to search?",
    )



class FilterForm(forms.Form):
    class_level = forms.ModelChoiceField(
        queryset=ClassLevel.objects.all(),
        label="Class",
        widget=forms.Select(attrs={'class': 'form-select'})   # ← no “select2”
    )

    # single-choice fields: keep Bootstrap look
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        required=False,
        label="Subject",
        widget=forms.Select(attrs={'class': 'form-select'})   # ← no “select2”
    )
    strand = forms.ModelChoiceField(
        queryset=Strand.objects.none(),
        required=False,
        label="Strand",
        widget=forms.Select(attrs={'class': 'form-select'})   # ← no “select2”
    )
    substrand = forms.ModelChoiceField(
        queryset=SubStrand.objects.none(),
        required=False,
        label="Sub-strand",
        widget=forms.Select(attrs={'class': 'form-select'})   # ← no “select2”
    )

    term = forms.ChoiceField(
        choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")],
        required=False,
        label="Term",
    )

    # key-area route
    key_area   = forms.ModelChoiceField(KeyLearningArea.objects.all(), required=False, label="Key area")

    # competency route
    competency = forms.ModelChoiceField(CoreCompetency.objects.all(), required=False, label="Competency")

    # theme route
    theme      = forms.ModelChoiceField(Theme.objects.all(), required=False, label="Theme")

    # resource-type route
    resource_type = forms.ModelChoiceField(ResourceType.objects.all(),
                                           required=False, label="Resource type")

    # quick-goal route
    goal       = forms.ModelChoiceField(GoalTag.objects.all(), required=False, label="Lesson goal")

    standard = forms.ModelChoiceField(
        queryset=ContentStandard.objects.none(),
        required=False,
        label="Content Standard",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    indicator = forms.ModelChoiceField(
        queryset=Indicator.objects.none(),
        required=False,
        label="Indicator",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    intended_use = forms.ChoiceField(choices=INTENDED_CHOICES, required=False, label="Purpose in lesson")
    time_needed = forms.ChoiceField(choices=TIME_NEEDED_CHOICES, required=False, label="Time in lesson")
    class_size  = forms.ChoiceField(choices=CLASS_SIZE_BANDS, required=False, label="Class size")
    bloom_level = forms.ChoiceField(choices=BLOOM_LEVELS, required=False, label="Bloom focus")
    budget_band = forms.ChoiceField(choices=BUDGET_BANDS, required=False, label="Budget band")
    learning_styles = forms.ModelMultipleChoiceField(
        queryset=LearningStyle.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Learning Styles",
    )
    special_needs = forms.ModelMultipleChoiceField(
        queryset=SpecialNeed.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Special Needs",
    )
    materials_available = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        label="Materials on hand",
    )
    learner_type = forms.ChoiceField(
    choices=SPECIAL_NEEDS_CHOICES,
    required=False,
    label="Learning difficulty",
    widget=forms.Select(attrs={"class": "form-select"})
    )

    preferred_format = forms.CharField(required=False, label="Preferred TLR format")
    classroom_setup  = forms.CharField(required=False, label="Classroom setup")
    outcome          = forms.CharField(required=False, widget=forms.Textarea,
                                       label="Learning outcome / indicator")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget
            base = widget.attrs.get('class', '')
            if isinstance(widget, forms.Select):
                widget.attrs['class'] = f'{base} form-select'.strip()
            elif isinstance(widget, forms.TextInput):
                widget.attrs['class'] = f'{base} form-control'.strip()
            elif isinstance(widget, forms.Textarea):
                widget.attrs['class'] = f'{base} form-control'.strip()
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = f'{base} form-check-input'.strip()
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs['class'] = f'{base} form-check-input'.strip()


        # limit Subject list after class_level picked
        if "class_level" in self.data:
            try:
                cls_id = int(self.data["class_level"])
                self.fields["subject"].queryset = Subject.objects.filter(class_level_id=cls_id)
            except (TypeError, ValueError):
                pass

        # limit Strand list after subject picked
        if "subject" in self.data:
            try:
                sub_id = int(self.data["subject"])
                self.fields["strand"].queryset = Strand.objects.filter(subject_id=sub_id)
            except (TypeError, ValueError):
                pass

        # limit Sub-strand list after strand picked
        if "strand" in self.data:
            try:
                strand_id = int(self.data["strand"])
                self.fields["substrand"].queryset = SubStrand.objects.filter(strand_id=strand_id)
            except (TypeError, ValueError):
                pass

        if "substrand" in self.data:
            try:
                substrand_id = int(self.data["substrand"])
                self.fields["standard"].queryset = ContentStandard.objects.filter(substrand_id=substrand_id)
            except (TypeError, ValueError):
                pass

        # limit Indicator list after standard picked
        if "standard" in self.data:
            try:
                std_id = int(self.data["standard"])
                self.fields["indicator"].queryset = Indicator.objects.filter(standard_id=std_id)
            except (TypeError, ValueError):
                pass


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

# In suggestor/forms.py, add this form:

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label="Phone Number (Optional)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+233 XX XXX XXXX'})
    )
    organization = forms.CharField(
        max_length=150,
        required=False,
        label="School/Organization (Optional)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your school or organization'})
    )
    subject = forms.ChoiceField(
        choices=[
            ('general', 'General Inquiry'),
            ('support', 'Technical Support'),
            ('pricing', 'Pricing & Plans'),
            ('training', 'TEDD Training'),
            ('feedback', 'Feedback'),
            ('partnership', 'Partnership Opportunity'),
        ],
        label="Subject",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 6, 
            'placeholder': 'Please share your message, feedback, or inquiry...'
        })
    )