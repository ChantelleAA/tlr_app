from django import forms

from .models import ClassLevel, Strand, SubStrand, Material

class TLRQueryForm(forms.Form):
    class_level = forms.ModelChoiceField(
        queryset=ClassLevel.objects.all(),
        label="Class",
    )
    strand = forms.ModelChoiceField(
        queryset=Strand.objects.none(),          # empty by default
        label="Strand",
    )
    sub_strand = forms.ModelChoiceField(
        queryset=SubStrand.objects.none(),
        label="Sub-strand / Topic",
        required=False,
    )
    # … (materials, learner type, etc.) …

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "class_level" in self.data:
            try:
                cls_id = int(self.data.get("class_level"))
                self.fields["strand"].queryset = Strand.objects.filter(class_level_id=cls_id)
            except (ValueError, TypeError):
                pass
        if "strand" in self.data:
            try:
                strand_id = int(self.data.get("strand"))
                self.fields["sub_strand"].queryset = SubStrand.objects.filter(strand_id=strand_id)
            except (ValueError, TypeError):
                pass
