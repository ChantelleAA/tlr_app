from .models import Tlr

def find_matches(data, route):
    qs = Tlr.objects.filter(class_level=data["class_level"])

    if route == "curriculum":
        if data.get("indicator"):
            qs = qs.filter(indicator=data["indicator"])
        elif data.get("substrand"):
            qs = qs.filter(substrand=data["substrand"])
        elif data.get("strand"):
            qs = qs.filter(strand=data["strand"])
        elif data.get("subject"):
            qs = qs.filter(subject=data["subject"])
        if data.get("term"):
            qs = qs.filter(term=data["term"])

    elif route == "key_area":
        qs = qs.filter(key_learning_areas=data["key_area"])

    elif route == "competency":
        qs = qs.filter(competencies=data["competency"])

    elif route == "theme":
        qs = qs.filter(themes=data["theme"])

    elif route == "resource":
        qs = qs.filter(resource_types=data["resource_type"])

    elif route == "goal":
        qs = qs.filter(goals=data["goal"])

    # … apply materials/time/budget scoring as before …
    return qs[:10]


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

