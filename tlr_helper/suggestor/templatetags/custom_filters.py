from django import template
import re

register = template.Library()

@register.filter
def youtube_embed(url):
    """Convert YouTube URL to embed format"""
    if not url:
        return url
    
    # Extract video ID from various YouTube URL formats
    youtube_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(youtube_regex, url)
    
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    
    return url  # Return original URL if not YouTube

@register.filter
def youtube_thumbnail(url):
    """Get YouTube thumbnail URL from video URL"""
    if not url:
        return ""
    
    # Extract video ID from various YouTube URL formats
    youtube_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(youtube_regex, url)
    
    if match:
        video_id = match.group(1)
        # YouTube provides several thumbnail qualities: default, hqdefault, maxresdefault
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    return ""  # Return empty if not YouTube

@register.filter
def youtube_video_id(url):
    """Extract just the video ID from YouTube URL"""
    if not url:
        return ""
    
    youtube_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(youtube_regex, url)
    
    if match:
        return match.group(1)
    
    return ""