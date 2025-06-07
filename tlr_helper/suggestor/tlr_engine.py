from django.db.models import Q
from .models import Tlr
import re

def find_matches(data, routes=None, keywords=None):
    """
    Enhanced TLR matching with keyword search and multiple route support.
    
    Args:
        data: Form data dictionary
        routes: List of routes or single route string (for backward compatibility)
        keywords: Keyword search string
    """
    qs = Tlr.objects.filter(is_published=True)
    
    # Handle backward compatibility - if routes is a string, convert to list
    if isinstance(routes, str):
        routes = [routes]
    elif routes is None:
        routes = []
    
    # KEYWORD SEARCH - takes priority
    if keywords:
        keyword_query = build_keyword_query(keywords)
        qs = qs.filter(keyword_query).distinct()
        
        # If we have keywords, apply basic filters and return
        qs = apply_basic_filters(qs, data)
        return rank_results(qs, data, keywords=keywords)
    
    # ROUTE-BASED SEARCH
    if not routes:
        # No routes selected, return empty or all results with basic filters
        qs = apply_basic_filters(qs, data)
        return rank_results(qs, data)
    
    # Apply filters for each selected route (OR logic between routes)
    route_queries = []
    
    for route in routes:
        route_qs = build_route_query(route, data)
        if route_qs is not None:
            route_queries.append(route_qs)
    
    # Combine route queries with OR logic
    if route_queries:
        combined_query = route_queries[0]
        for query in route_queries[1:]:
            combined_query |= query
        qs = qs.filter(combined_query).distinct()
    
    # Apply common filters
    qs = apply_basic_filters(qs, data)
    
    return rank_results(qs, data)


def build_keyword_query(keywords):
    """
    Build a comprehensive Q object for keyword search across multiple fields.
    """
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
    """
    Build query for a specific route based on form data.
    """
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
    """
    Build curriculum hierarchy query with proper precedence.
    """
    if data.get("indicator"):
        query = Q(indicator=data["indicator"])
    elif data.get("standard"):
        query = Q(standard=data["standard"])
    elif data.get("substrand"):
        query = Q(substrand=data["substrand"])
    elif data.get("strand"):
        query = Q(strand=data["strand"])
    elif data.get("subject"):
        query = Q(subject=data["subject"])
    elif data.get("class_level"):
        query = Q(class_level=data["class_level"])
    else:
        return None
    
    # Add term filter if specified
    if data.get("term"):
        query &= Q(term=data["term"])
    
    return query


def apply_basic_filters(qs, data):
    """
    Apply common filters that work regardless of route.
    """
    # Time filter
    if data.get("time_needed"):
        qs = qs.filter(time_needed=data["time_needed"])
    
    # Budget filter
    if data.get("budget_band"):
        qs = qs.filter(budget_band=data["budget_band"])
    
    # Class level (if not already filtered by curriculum route)
    if data.get("class_level") and not any(data.get(f) for f in ["indicator", "standard", "substrand", "strand", "subject"]):
        qs = qs.filter(class_level=data["class_level"])
    
    # Intended use
    if data.get("intended_use"):
        qs = qs.filter(intended_use=data["intended_use"])
    
    # Bloom level
    if data.get("bloom_level"):
        qs = qs.filter(bloom_level=data["bloom_level"])
    
    # Class size
    if data.get("class_size"):
        qs = qs.filter(class_size=data["class_size"])
    
    # Learning styles (many-to-many)
    if data.get("learning_styles"):
        for style in data["learning_styles"]:
            qs = qs.filter(learning_styles=style)
    
    # Special needs (many-to-many)
    if data.get("special_needs"):
        for need in data["special_needs"]:
            qs = qs.filter(special_needs=need)
    
    # Materials available
    if data.get("materials_available"):
        for material in data["materials_available"]:
            qs = qs.filter(materials=material)
    
    return qs


def rank_results(qs, data, keywords=None):
    """
    Advanced scoring and ranking of TLR results.
    """
    def score(tlr):
        score = 0
        
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
        if tlr.images.exists():
            score += 1
        if tlr.videos.exists():
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