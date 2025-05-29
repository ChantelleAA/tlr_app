# suggestor/forms.py
from django import forms
from .models import (
    ClassLevel, Strand, SubStrand, Material,
    INTENDED_CHOICES, TIME_CHOICES,
    CLASS_SIZE_BANDS, BLOOM_LEVELS, BUDGET_BANDS,
)


class TLRQueryForm(forms.Form):
    # ------------------ cascade section ------------------
    class_level = forms.ModelChoiceField(
        queryset=ClassLevel.objects.all(),
        label="Class level",
    )
    strand = forms.ModelChoiceField(
        queryset=Strand.objects.none(),
        label="Strand",
    )
    sub_strand = forms.ModelChoiceField(
        queryset=SubStrand.objects.none(),
        label="Sub-strand / topic",
        required=False,
    )

    # ------------------ basic specifics ------------------
    intended_use = forms.ChoiceField(
        choices=INTENDED_CHOICES,
        label="Purpose in lesson",
    )
    time_available = forms.ChoiceField(
        choices=TIME_CHOICES,
        required=False,
        label="Time in lesson",
    )

    # ------------------ advanced section -----------------
    class_size = forms.ChoiceField(
        choices=CLASS_SIZE_BANDS,
        required=False,
        label="Class size",
    )
    bloom_level = forms.ChoiceField(
        choices=BLOOM_LEVELS,
        required=False,
        label="Bloom’s focus",
    )
    budget_band = forms.ChoiceField(
        choices=BUDGET_BANDS,
        required=False,
        label="Budget per lesson (GHS)",
    )
    materials_available = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Materials on hand",
    )
    learner_type = forms.CharField(
        required=False,
        label="Special-needs notes",
        help_text="e.g. early readers, low vision",
    )
    preferred_format = forms.CharField(
        required=False,
        label="Preferred TLR format",
        help_text="poster, puzzle, slider …",
    )
    classroom_setup = forms.CharField(
        required=False,
        label="Classroom setup",
        help_text="no wall space, outdoor, group tables …",
    )
    outcome = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Learning outcome / indicator",
    )

    # ---------- dynamic dropdown logic ----------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # populate strand list once class is chosen
        if "class_level" in self.data:
            try:
                cls_id = int(self.data["class_level"])
                self.fields["strand"].queryset = Strand.objects.filter(
                    class_level_id=cls_id
                )
            except (ValueError, TypeError):
                pass

        # populate sub-strand list once strand is chosen
        if "strand" in self.data:
            try:
                st_id = int(self.data["strand"])
                self.fields["sub_strand"].queryset = SubStrand.objects.filter(
                    strand_id=st_id
                )
            except (ValueError, TypeError):
                pass
