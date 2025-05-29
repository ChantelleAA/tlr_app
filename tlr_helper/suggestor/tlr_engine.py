from .models import Tlr

# suggestor/tlr_engine.py
from .models import Tlr


def find_matches(data):
    """
    Return a ranked list of up to 10 TLR objects that match teacher inputs.
    """

    # ---------- 1. mandatory filters ----------
    qs = (
        Tlr.objects
        .filter(class_level=data["class_level"])
        .filter(strand__icontains=data["strand"])
        .filter(intended_use=data["intended_use"])
        .distinct()
    )

    # ---------- 2. materials filter ----------
    materials = data.get("materials_available")
    if materials:
        qs = qs.filter(materials__in=materials).distinct()

    # ---------- 3. budget & class-size constraints ----------
    if data.get("budget_band") == "low":
        qs = qs.exclude(costly=True)
    if data.get("class_size") == "large":
        qs = qs.exclude(tlr_type="small-group-only")

    # ---------- 4. scoring ----------
    def score(tlr):
        s = 0
        # match on time in lesson
        if data.get("time_available") and tlr.time_needed == data["time_available"]:
            s += 2
        # match on Bloom level
        if data.get("bloom_level") and getattr(tlr, "bloom", "") == data["bloom_level"]:
            s += 2
        # match on preferred format
        if data.get("preferred_format") and data["preferred_format"].lower() in tlr.tlr_type.lower():
            s += 1
        return s

    ranked = sorted(qs, key=score, reverse=True)
    return ranked[:10]


def score(tlr, data):
    score = 0
    if data.get("time_available") and tlr.time_needed == data["time_available"]:
        score += 2
    if data.get("learner_type") and data["learner_type"].lower() in tlr.accessibility_notes.lower():
        score += 1
    return score

