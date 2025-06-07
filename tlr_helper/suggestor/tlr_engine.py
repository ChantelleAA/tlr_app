from django.db.models import Q
from .models import Tlr
import re

def find_matches(data, routes=None, keywords=None):
    """Enhanced TLR matching - FLEXIBLE, not restrictive!"""
    qs = Tlr.objects.filter(is_published=True)
    
    # Handle backward compatibility
    if isinstance(routes, str):
        routes = [routes]
    elif routes is None:
        routes = []
    
    print(f"DEBUG find_matches: routes={routes}, data keys={list(data.keys())}")
    print(f"DEBUG find_matches: Starting with {qs.count()} published TLRs")
    
    # KEYWORD SEARCH - takes priority
    if keywords:
        keyword_query = build_keyword_query(keywords)
        qs = qs.filter(keyword_query).distinct()
        qs = apply_basic_filters(qs, data)
        return rank_results(qs, data, keywords=keywords)
    
    # ROUTE-BASED SEARCH
    if not routes:
        print("DEBUG: No routes, applying basic filters only")
        qs = apply_basic_filters(qs, data)
        results = rank_results(qs, data)
        print(f"DEBUG: No routes - returning {len(results)} TLRs")
        return results
    
    # Apply filters for each selected route (OR logic between routes)
    route_queries = []
    
    for route in routes:
        print(f"DEBUG: Processing route '{route}'")
        route_qs = build_route_query(route, data)
        if route_qs is not None:
            route_queries.append(route_qs)
            print(f"DEBUG: Added query for route '{route}'")
        else:
            print(f"DEBUG: No query built for route '{route}' - will include all TLRs for this route")
    
    # If we have route queries, combine them
    if route_queries:
        combined_query = route_queries[0]
        for query in route_queries[1:]:
            combined_query |= query
        qs = qs.filter(combined_query).distinct()
        print(f"DEBUG: Combined route queries, found {qs.count()} TLRs")
    else:
        print("DEBUG: No specific route queries - keeping all TLRs")
    
    # Apply common filters
    qs = apply_basic_filters(qs, data)
    results = rank_results(qs, data)
    print(f"DEBUG: Final result count: {len(results)}")
    
    return results


def build_keyword_query(keywords):
    """Build a comprehensive Q object for keyword search across multiple fields."""
    if not keywords:
        return Q()
    
    # Clean and split keywords
    keyword_list = [k.strip() for k in re.split(r'[,\s]+', keywords.lower()) if k.strip()]
    
    query = Q()
    
    for keyword in keyword_list:
        # Search across all relevant text fields
        keyword_q = (
            Q(title__icontains=keyword) |
            Q(brief_description__icontains=keyword) |
            Q(steps_to_make__icontains=keyword) |
            Q(tips_for_use__icontains=keyword) |
            Q(learning_outcome__icontains=keyword) |
            Q(search_keywords__icontains=keyword) |
            
            # Search in related fields
            Q(materials__name__icontains=keyword) |
            Q(themes__title__icontains=keyword) |
            Q(key_learning_areas__title__icontains=keyword) |
            Q(competencies__title__icontains=keyword) |
            Q(resource_types__title__icontains=keyword) |
            Q(special_needs__name__icontains=keyword) |
            Q(learning_styles__name__icontains=keyword) |
            
            # Search in curriculum fields
            Q(subject__title__icontains=keyword) |
            Q(strand__title__icontains=keyword) |
            Q(substrand__title__icontains=keyword) |
            Q(standard__description__icontains=keyword) |
            Q(indicator__description__icontains=keyword)
        )
        
        query &= keyword_q  # AND logic between different keywords
    
    return query


def build_route_query(route, data):
    """Build query for a specific route based on form data."""
    if route == "curriculum":
        return build_curriculum_query(data)
    elif route == "key_area" and data.get("key_area"):
        return Q(key_learning_areas=data["key_area"])
    elif route == "competency" and data.get("competency"):
        return Q(competencies=data["competency"])
    elif route == "theme" and data.get("theme"):
        return Q(themes=data["theme"])
    elif route == "resource" and data.get("resource_type"):
        return Q(resource_types=data["resource_type"])
    elif route == "goal" and data.get("goal"):
        return Q(goals=data["goal"])
    
    return None


def build_curriculum_query(data):
    """Find TLRs that match ANY curriculum criteria you selected."""
    curriculum_queries = []
    
    # Build separate queries for each thing you selected
    if data.get("class_level"):
        curriculum_queries.append(Q(class_level=data["class_level"]))
        print(f"DEBUG: Will look for TLRs with class_level={data['class_level']}")
    
    if data.get("subject"):
        curriculum_queries.append(Q(subject=data["subject"]))
        print(f"DEBUG: Will look for TLRs with subject={data['subject']}")
        
    if data.get("term"):
        curriculum_queries.append(Q(term=data["term"]))
        print(f"DEBUG: Will look for TLRs with term={data['term']}")
        
    if data.get("strand"):
        curriculum_queries.append(Q(strand=data["strand"]))
        print(f"DEBUG: Will look for TLRs with strand={data['strand']}")
        
    if data.get("substrand"):
        curriculum_queries.append(Q(substrand=data["substrand"]))
        print(f"DEBUG: Will look for TLRs with substrand={data['substrand']}")
        
    if data.get("standard"):
        curriculum_queries.append(Q(standard=data["standard"]))
        print(f"DEBUG: Will look for TLRs with standard={data['standard']}")
        
    if data.get("indicator"):
        curriculum_queries.append(Q(indicator=data["indicator"]))
        print(f"DEBUG: Will look for TLRs with indicator={data['indicator']}")
    
    # If no curriculum criteria selected, match all
    if not curriculum_queries:
        print(f"DEBUG: No curriculum criteria - will show all TLRs")
        return Q()  # Empty Q matches everything
    
    # Combine with OR logic - match TLRs that have ANY of these
    combined_query = curriculum_queries[0]
    for query in curriculum_queries[1:]:
        combined_query |= query  # OR logic
    
    print(f"DEBUG: Looking for TLRs that match ANY of {len(curriculum_queries)} curriculum criteria")
    return combined_query

def apply_basic_filters(qs, data):
    """Only apply filters if user actually selected something (not defaults)"""
    
    # Skip common default values - only filter if user made a real choice
    if data.get("time_needed") and data.get("time_needed") not in ["", "starter"]:
        qs = qs.filter(time_needed=data["time_needed"])
        print(f"DEBUG: Applied time_needed filter: {data['time_needed']}, remaining: {qs.count()}")
    
    if data.get("budget_band") and data.get("budget_band") not in ["", "none"]:
        qs = qs.filter(budget_band=data["budget_band"])
        print(f"DEBUG: Applied budget_band filter: {data['budget_band']}, remaining: {qs.count()}")
    
    if data.get("intended_use") and data.get("intended_use") not in ["", "intro"]:
        qs = qs.filter(intended_use=data["intended_use"])
        print(f"DEBUG: Applied intended_use filter: {data['intended_use']}, remaining: {qs.count()}")
    
    if data.get("bloom_level") and data.get("bloom_level") not in ["", "remember"]:
        qs = qs.filter(bloom_level=data["bloom_level"])
        print(f"DEBUG: Applied bloom_level filter: {data['bloom_level']}, remaining: {qs.count()}")
    
    if data.get("class_size") and data.get("class_size") not in ["", "small"]:
        qs = qs.filter(class_size=data["class_size"])
        print(f"DEBUG: Applied class_size filter: {data['class_size']}, remaining: {qs.count()}")
    
    # Other filters stay the same...
    
    return qs

# def apply_basic_filters(qs, data):
#     """Apply common filters - but only if they're specifically selected (not default values)"""
    
#     # Only apply filters if user specifically selected them (not just form defaults)
    
#     # Time filter - only if specifically selected
#     if data.get("time_needed") and data.get("time_needed") != "":
#         qs = qs.filter(time_needed=data["time_needed"])
#         print(f"DEBUG: Applied time_needed filter: {data['time_needed']}, remaining: {qs.count()}")
    
#     # Budget filter - only if specifically selected 
#     if data.get("budget_band") and data.get("budget_band") != "" and data.get("budget_band") != "none":
#         qs = qs.filter(budget_band=data["budget_band"])
#         print(f"DEBUG: Applied budget_band filter: {data['budget_band']}, remaining: {qs.count()}")
    
#     # Intended use - only if specifically selected
#     if data.get("intended_use") and data.get("intended_use") != "":
#         qs = qs.filter(intended_use=data["intended_use"])
#         print(f"DEBUG: Applied intended_use filter: {data['intended_use']}, remaining: {qs.count()}")
    
#     # Bloom level - only if specifically selected
#     if data.get("bloom_level") and data.get("bloom_level") != "":
#         qs = qs.filter(bloom_level=data["bloom_level"])
#         print(f"DEBUG: Applied bloom_level filter: {data['bloom_level']}, remaining: {qs.count()}")
    
#     # Class size - only if specifically selected
#     if data.get("class_size") and data.get("class_size") != "":
#         qs = qs.filter(class_size=data["class_size"])
#         print(f"DEBUG: Applied class_size filter: {data['class_size']}, remaining: {qs.count()}")
    
#     # Learning styles (many-to-many) - only if any selected
#     if data.get("learning_styles") and data.get("learning_styles").exists():
#         for style in data["learning_styles"]:
#             qs = qs.filter(learning_styles=style)
#         print(f"DEBUG: Applied learning_styles filter, remaining: {qs.count()}")
    
#     # Special needs (many-to-many) - only if any selected
#     if data.get("special_needs") and data.get("special_needs").exists():
#         for need in data["special_needs"]:
#             qs = qs.filter(special_needs=need)
#         print(f"DEBUG: Applied special_needs filter, remaining: {qs.count()}")
    
#     # Materials available - only if any selected
#     if data.get("materials_available") and data.get("materials_available").exists():
#         for material in data["materials_available"]:
#             qs = qs.filter(materials=material)
#         print(f"DEBUG: Applied materials_available filter, remaining: {qs.count()}")
    
#     print(f"DEBUG: Final count after basic filters: {qs.count()}")
#     return qs

def rank_results(qs, data, keywords=None):
    """Rank TLRs - ones matching more criteria come first"""
    def score(tlr):
        score = 0
        
        # Curriculum matching bonus - more matches = higher score
        curriculum_matches = 0
        if data.get("class_level") and tlr.class_level == data["class_level"]:
            curriculum_matches += 1
        if data.get("subject") and tlr.subject == data["subject"]:
            curriculum_matches += 1
        if data.get("term") and tlr.term == data.get("term"):
            curriculum_matches += 1
        if data.get("strand") and tlr.strand == data["strand"]:
            curriculum_matches += 1
        if data.get("substrand") and tlr.substrand == data["substrand"]:
            curriculum_matches += 1
        if data.get("standard") and tlr.standard == data["standard"]:
            curriculum_matches += 1
        if data.get("indicator") and tlr.indicator == data["indicator"]:
            curriculum_matches += 1
        
        # Give big bonus for curriculum matches
        score += curriculum_matches * 10
        
        # Keyword relevance scoring
        if keywords:
            keyword_list = [k.strip().lower() for k in re.split(r'[,\s]+', keywords) if k.strip()]
            
            # Title matches get highest score
            for keyword in keyword_list:
                if keyword in tlr.title.lower():
                    score += 10
                if keyword in tlr.brief_description.lower():
                    score += 5
                if keyword in (tlr.steps_to_make or "").lower():
                    score += 3
                if keyword in (tlr.tips_for_use or "").lower():
                    score += 3
        
        # Preference matching
        if data.get("time_needed") and tlr.time_needed == data["time_needed"]:
            score += 5
        
        if data.get("budget_band") and tlr.budget_band == data["budget_band"]:
            score += 3
        
        if data.get("intended_use") and tlr.intended_use == data["intended_use"]:
            score += 4
        
        # Popularity factor
        score += min(tlr.download_count * 0.1, 5)  # Cap at 5 points
        
        # Completeness factor (TLRs with more info rank higher)
        if tlr.steps_to_make:
            score += 2
        if tlr.tips_for_use:
            score += 2
        if hasattr(tlr, 'images') and tlr.images.exists():
            score += 1
        if hasattr(tlr, 'videos') and tlr.videos.exists():
            score += 2
        
        return score
    
    # Sort by score and limit results
    sorted_results = sorted(qs, key=score, reverse=True)
    
    # Return top 20 results for performance
    return sorted_results[:20]


# Keep the original function for backward compatibility
def find_matches_legacy(data, route):
    """Legacy function for backward compatibility."""
    return find_matches(data, routes=[route] if route else [])