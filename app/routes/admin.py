from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import login_required
from app.repositories.url_repo import url_repo
from app.services.url_service import validate_url_data, prepare_url_data, validate_url_collection

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required
def dashboard():
    """Admin dashboard page"""
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
    
    # Get stats
    stats = url_repo.get_stats()
    
    return render_template(
        'dashboard.html',
        urls=result['urls'],
        total=result['total'],
        page=result['page'],
        pages=result['pages'],
        search=search,
        selected_tag=tag,
        stats=stats
    )


@bp.route('/url/new', methods=['GET', 'POST'])
@login_required
def create_url():
    """Create new URL collection with multiple URLs"""
    if request.method == 'POST':
        # Get collection-level data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        tags = request.form.get('tags', '').strip()
        
        # Get arrays of URLs and subtitles
        urls = request.form.getlist('urls[]')
        subtitles = request.form.getlist('subtitles[]')
        
        # Build URL array with subtitles
        url_array = []
        for i in range(len(urls)):
            if urls[i].strip():  # Only add non-empty URLs
                url_array.append({
                    'url': urls[i].strip(),
                    'subtitle': subtitles[i].strip() if i < len(subtitles) else ''
                })
        
        if not url_array:
            flash('At least one URL is required', 'error')
        elif not title:
            flash('Title is required', 'error')
        else:
            # Validate and prepare data
            from app.services.url_service import validate_url_collection
            is_valid, errors = validate_url_collection({
                'title': title,
                'description': description,
                'tags': tags,
                'urls': url_array
            })
            
            if is_valid:
                # Prepare and save data
                url_data = prepare_url_data({
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'urls': url_array
                })
                result = url_repo.create(url_data)
                
                if result:
                    flash(f'Collection with {len(url_array)} URL(s) added successfully!', 'success')
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash('Failed to create collection', 'error')
            else:
                # Show validation errors
                for field, error in errors.items():
                    flash(f'{field.title()}: {error}', 'error')
    
    return render_template('url_form.html', url=None, mode='create')


@bp.route('/url/<url_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_url(url_id):
    """Edit existing URL"""
    url = url_repo.find_by_id(url_id)
    
    if not url:
        flash('URL not found', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        # Detect collection edit (urls[] present)
        urls_list = request.form.getlist('urls[]')
        subtitles_list = request.form.getlist('subtitles[]')
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        tags = request.form.get('tags', '').strip()

        has_collection = any(u.strip() for u in urls_list)

        if has_collection:
            # Build collection items
            url_items = []
            for i, raw_url in enumerate(urls_list):
                raw_url = raw_url.strip()
                if not raw_url:
                    continue
                subtitle = subtitles_list[i].strip() if i < len(subtitles_list) else ''
                url_items.append({'url': raw_url, 'subtitle': subtitle})

            if not url_items:
                flash('At least one URL is required', 'error')
            elif not title:
                flash('Title is required', 'error')
            else:
                # Validate collection
                is_valid, errors = validate_url_collection({
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'urls': url_items
                })

                if is_valid:
                    update_data = prepare_url_data({
                        'title': title,
                        'description': description,
                        'tags': tags,
                        'urls': url_items
                    })
                    success = url_repo.update(url_id, update_data)
                    if success:
                        flash(f'Collection updated successfully with {len(url_items)} URL(s)!', 'success')
                        return redirect(url_for('admin.dashboard'))
                    else:
                        flash('Failed to update collection', 'error')
                else:
                    for field, error in errors.items():
                        flash(f'{field.title()}: {error}', 'error')
        else:
            # Fallback to single URL update
            is_valid, errors = validate_url_data(request.form)

            if is_valid:
                update_data = prepare_url_data(request.form)
                success = url_repo.update(url_id, update_data)
                if success:
                    flash('URL updated successfully!', 'success')
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash('Failed to update URL', 'error')
            else:
                for field, error in errors.items():
                    flash(f'{field.title()}: {error}', 'error')
    
    return render_template('url_form.html', url=url, mode='edit')


@bp.route('/url/<url_id>/delete', methods=['POST'])
@login_required
def delete_url(url_id):
    """Delete URL"""
    success = url_repo.delete(url_id)
    
    if success:
        flash('URL deleted successfully!', 'success')
    else:
        flash('Failed to delete URL', 'error')
    
    return redirect(url_for('admin.dashboard'))
