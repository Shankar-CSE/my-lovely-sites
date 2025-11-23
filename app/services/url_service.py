import re
from urllib.parse import urlparse


def normalize_tags(tags_input):
    """
    Normalize tags from comma-separated string to list
    - Converts to lowercase
    - Strips whitespace
    - Removes duplicates
    - Filters empty strings
    """
    if not tags_input:
        return []
    
    if isinstance(tags_input, list):
        tags = tags_input
    else:
        tags = [tag.strip() for tag in tags_input.split(',')]
    
    # Normalize: lowercase, strip, remove empty, remove duplicates
    normalized = []
    seen = set()
    
    for tag in tags:
        tag = tag.lower().strip()
        if tag and tag not in seen:
            normalized.append(tag)
            seen.add(tag)
    
    return normalized


def validate_url(url):
    """
    Validate URL format
    Returns (is_valid, error_message)
    """
    if not url:
        return False, "URL is required"
    
    if len(url) > 2048:
        return False, "URL is too long"
    
    # Basic URL pattern
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False, "Invalid URL format. Must start with http:// or https://"
    
    return True, None


def validate_url_data(data):
    """
    Validate URL form data
    Returns (is_valid, errors_dict)
    """
    errors = {}
    
    # Validate URL
    url = data.get('url', '').strip()
    is_valid, error = validate_url(url)
    if not is_valid:
        errors['url'] = error
    
    # Validate title
    title = data.get('title', '').strip()
    if not title:
        errors['title'] = "Title is required"
    elif len(title) > 200:
        errors['title'] = "Title is too long (max 200 characters)"
    
    # Validate description (optional)
    description = data.get('description', '').strip()
    if description and len(description) > 1000:
        errors['description'] = "Description is too long (max 1000 characters)"
    
    # Validate tags (optional)
    tags = normalize_tags(data.get('tags', ''))
    if len(tags) > 20:
        errors['tags'] = "Too many tags (max 20)"
    
    return len(errors) == 0, errors


def prepare_url_data(form_data):
    """
    Prepare URL data from form for storage
    """
    return {
        'url': form_data.get('url', '').strip(),
        'title': form_data.get('title', '').strip(),
        'description': form_data.get('description', '').strip(),
        'tags': normalize_tags(form_data.get('tags', ''))
    }


def get_domain(url):
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ''
