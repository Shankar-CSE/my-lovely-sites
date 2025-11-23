from flask import Blueprint, render_template, request
from app.repositories.url_repo import url_repo

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    """Public URL catalog page"""
    # Get query parameters
    search = request.args.get('q', '').strip()
    tag = request.args.get('tag', '').strip()
    page = request.args.get('page', 1, type=int)
    
    # Get URLs with filters
    result = url_repo.find_all(
        search=search if search else None,
        tag=tag if tag else None,
        page=page,
        per_page=24
    )
    
    # Get all tags for filter
    all_tags = url_repo.get_all_tags()
    
    return render_template(
        'index.html',
        urls=result['urls'],
        total=result['total'],
        page=result['page'],
        pages=result['pages'],
        search=search,
        selected_tag=tag,
        all_tags=all_tags
    )
