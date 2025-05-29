from .models import Tlr

def find_matches(data):
    qs = Tlr.objects.filter(
        strand__icontains=data["strand"],
        class_level=data["class_level"],
        intended_use=data["intended_use"],
    )
    if materials := data.get("materials_available"):
        qs = qs.filter(materials__in=materials).distinct()
    if pf := data.get("preferred_format"):
        qs = qs.filter(tlr_type__icontains=pf)
    # simple ranking: quick activities first if teacher said time is quick
    if data.get("time_available") == "quick":
        qs = qs.order_by("time_needed")
    return list(qs[:10])        # cap to 10 suggestions

def score(tlr, data):
    score = 0
    if data.get("time_available") and tlr.time_needed == data["time_available"]:
        score += 2
    if data.get("learner_type") and data["learner_type"].lower() in tlr.accessibility_notes.lower():
        score += 1
    return score

def find_matches(data):
    qs = Tlr.objects.filter(
        strand__icontains=data["strand"],
        class_level=data["class_level"],
        intended_use=data["intended_use"],
    ).distinct()

    if mats := data.get("materials_available"):
        qs = qs.filter(materials__in=mats).distinct()

    ranked = sorted(qs, key=lambda t: score(t, data), reverse=True)
    return ranked[:10]
