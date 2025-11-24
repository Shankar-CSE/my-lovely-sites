from flask import Blueprint, render_template, request
from app.repositories.url_repo import url_repo

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    """Public URL catalog page - displays all URLs"""
    # Get query parameters
    search = request.args.get('q', '').strip()
    tag = request.args.get('tag', '').strip()
    
    # Get all URLs with filters (no pagination)
    result = url_repo.find_all(
        search=search if search else None,
        tag=tag if tag else None,
        per_page=None  # Fetch all URLs
    )
    
    # Get all tags for filter
    all_tags = url_repo.get_all_tags()
    
    return render_template(
        'index.html',
        urls=result['urls'],
        total=result['total'],
        search=search,
        selected_tag=tag,
        all_tags=all_tags
    )
