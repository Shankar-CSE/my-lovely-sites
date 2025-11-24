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
    Validate URL form data (backward compatibility for single URLs)
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


def validate_url_collection(data):
    """
    Validate URL collection with array of URLs and subtitles
    Returns (is_valid, errors_dict)
    """
    errors = {}
    
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
    
    # Validate URLs array
    urls = data.get('urls', [])
    if not urls:
        errors['urls'] = "At least one URL is required"
    elif len(urls) > 10:
        errors['urls'] = "Maximum 10 URLs allowed per collection"
    else:
        # Validate each URL and subtitle
        for idx, url_item in enumerate(urls):
            url = url_item.get('url', '').strip()
            subtitle = url_item.get('subtitle', '').strip()
            
            is_valid_url, url_error = validate_url(url)
            if not is_valid_url:
                errors[f'url_{idx}'] = f"URL #{idx + 1}: {url_error}"
            
            if subtitle and len(subtitle) > 200:
                errors[f'subtitle_{idx}'] = f"Subtitle #{idx + 1} is too long (max 200 characters)"
    
    return len(errors) == 0, errors


def prepare_url_data(form_data):
    """
    Prepare URL data from form for storage
    """
    # Check if it's a URL collection with array
    if 'urls' in form_data and isinstance(form_data['urls'], list):
        return {
            'title': form_data.get('title', '').strip(),
            'description': form_data.get('description', '').strip(),
            'tags': normalize_tags(form_data.get('tags', '')),
            'urls': form_data['urls']  # Array of {url, subtitle}
        }
    else:
        # Backward compatibility for single URL
        return {
            'url': form_data.get('url', '').strip(),
            'title': form_data.get('title', '').strip(),
            'description': form_data.get('description', '').strip(),
            'tags': normalize_tags(form_data.get('tags', ''))
        }


def validate_batch(url_data_list, max_size=50):
    """
    Validate a batch of URL data items
    Returns (is_valid, valid_items, errors_list)
    """
    if len(url_data_list) > max_size:
        return False, [], [f'Batch size exceeds maximum of {max_size} URLs']
    
    if len(url_data_list) == 0:
        return False, [], ['No URLs provided']
    
    valid_items = []
    errors_list = []
    
    for idx, data in enumerate(url_data_list):
        is_valid, errors = validate_url_data(data)
        if is_valid:
            valid_items.append(data)
        else:
            error_msg = f"URL #{idx + 1}: " + ", ".join([f"{k}: {v}" for k, v in errors.items()])
            errors_list.append(error_msg)
    
    return len(valid_items) > 0, valid_items, errors_list


def get_domain(url):
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return ''
