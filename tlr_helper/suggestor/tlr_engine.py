from .models import Tlr

def find_matches(data, route):
    """
    Filters TLRs based on the selected route and form data.
    Supports curriculum routes as well as tag-based filters (theme, competency, etc.).
    Applies basic publication filtering and optional scoring.
    """
    qs = Tlr.objects.all()

    # Route 1: Curriculum hierarchy
    if route == "curriculum":
        if data.get("indicator"):
            qs = qs.filter(indicator=data["indicator"])
        elif data.get("standard"):
            qs = qs.filter(standard=data["standard"])
        elif data.get("substrand"):
            qs = qs.filter(substrand=data["substrand"])
        elif data.get("strand"):
            qs = qs.filter(strand=data["strand"])
        elif data.get("subject"):
            qs = qs.filter(subject=data["subject"])
        elif data.get("class_level"):
            qs = qs.filter(class_level=data["class_level"])

        if data.get("term"):
            qs = qs.filter(term=data["term"])

    # Route 2: Key Learning Area
    elif route == "key_area" and data.get("key_area"):
        qs = qs.filter(key_learning_areas=data["key_area"])

    # Route 3: Core Competency
    elif route == "competency" and data.get("competency"):
        qs = qs.filter(competencies=data["competency"])

    # Route 4: Theme
    elif route == "theme" and data.get("theme"):
        qs = qs.filter(themes=data["theme"])

    # Route 5: Resource Type
    elif route == "resource" and data.get("resource_type"):
        qs = qs.filter(resource_types=data["resource_type"])

    # Route 6: Goal Tag
    elif route == "goal" and data.get("goal"):
        qs = qs.filter(goals=data["goal"])

    # Optional: restrict to published only
    qs = qs.filter(is_published=True)

    # Optional: rank based on user preferences
    return rank_results(qs, data)


def rank_results(qs, data):
    """
    Scores and sorts TLRs based on user preferences like time, format, etc.
    """
    def score(tlr):
        s = 0
        # Match on time available
        if data.get("time_available") and tlr.time_needed == data["time_available"]:
            s += 2
        # Match on preferred format
        if data.get("preferred_format") and data["preferred_format"].lower() in (tlr.tlr_type or "").lower():
            s += 1
        return s

    return sorted(qs, key=score, reverse=True)[:10]
