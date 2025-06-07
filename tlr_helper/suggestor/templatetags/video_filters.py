from django import template
import re

register = template.Library()

@register.filter
def youtube_id(url):
    """Extract YouTube video ID from any YouTube URL format"""
    if not url:
        return ""
    
    # Remove any parameters and extract just the video ID
    # For embed URLs: https://www.youtube.com/embed/VIDEO_ID
    if '/embed/' in url:
        # Get everything after /embed/ and before any parameters
        video_id = url.split('/embed/')[-1].split('?')[0].split('&')[0]
        return video_id
    
    return ""

@register.filter 
def youtube_thumbnail(video_id):
    """Get YouTube thumbnail URL from video ID"""
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    return ""