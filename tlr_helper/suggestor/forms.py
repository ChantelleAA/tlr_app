# suggestor/forms.py
from django import forms
from .models import (
    # curriculum hierarchy
    ClassLevel, Subject, Strand, SubStrand,
    # optional tags
    Theme, KeyLearningArea, CoreCompetency, ResourceType, GoalTag,
    # supporting tables
    Material,
    # constants
    INTENDED_CHOICES, TIME_CHOICES,
    CLASS_SIZE_BANDS, BLOOM_LEVELS, BUDGET_BANDS,
)



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
    # always visible
    class_level = forms.ModelChoiceField(ClassLevel.objects.all(), label="Class")

    # curriculum route
    subject = forms.ModelChoiceField(Subject.objects.none(), required=False, label="Subject")

    term = forms.ChoiceField(
        choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")],
        required=False,
        label="Term",
    )
    strand     = forms.ModelChoiceField(Strand.objects.none(),   required=False, label="Strand")
    substrand  = forms.ModelChoiceField(SubStrand.objects.none(), required=False, label="Sub-strand")

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

    intended_use = forms.ChoiceField(choices=INTENDED_CHOICES, required=False, label="Purpose in lesson")
    time_available = forms.ChoiceField(choices=TIME_CHOICES, required=False, label="Time in lesson")
    class_size  = forms.ChoiceField(choices=CLASS_SIZE_BANDS, required=False, label="Class size")
    bloom_level = forms.ChoiceField(choices=BLOOM_LEVELS, required=False, label="Bloom focus")
    budget_band = forms.ChoiceField(choices=BUDGET_BANDS, required=False, label="Budget band")
    materials_available = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        label="Materials on hand",
    )
    learner_type = forms.CharField(required=False, label="Special-needs notes")
    preferred_format = forms.CharField(required=False, label="Preferred TLR format")
    classroom_setup  = forms.CharField(required=False, label="Classroom setup")
    outcome          = forms.CharField(required=False, widget=forms.Textarea,
                                       label="Learning outcome / indicator")

    # ───────────────────────────────────────────
    #  dynamic dropdown logic
    # ───────────────────────────────────────────
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'form-check-input'})

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
