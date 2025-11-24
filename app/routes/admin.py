from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import login_required
from app.repositories.url_repo import url_repo
from app.services.url_service import validate_url_data, prepare_url_data

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
    """Create new URL(s) - supports single or batch creation"""
    if request.method == 'POST':
        # Check if batch input (array fields)
        titles = request.form.getlist('title[]')
        urls = request.form.getlist('url[]')
        descriptions = request.form.getlist('description[]')
        tags = request.form.getlist('tags[]')
        
        # Batch mode: multiple URLs
        if titles and len(titles) > 1:
            from app.services.url_service import validate_batch
            
            # Build list of form data dicts
            url_data_list = []
            for i in range(len(titles)):
                url_data_list.append({
                    'title': titles[i] if i < len(titles) else '',
                    'url': urls[i] if i < len(urls) else '',
                    'description': descriptions[i] if i < len(descriptions) else '',
                    'tags': tags[i] if i < len(tags) else ''
                })
            
            # Validate batch
            has_valid, valid_items, error_list = validate_batch(url_data_list, max_size=50)
            
            if has_valid:
                # Prepare valid items
                prepared_items = [prepare_url_data(item) for item in valid_items]
                
                # Create batch
                results = url_repo.create_many(prepared_items)
                
                # Flash results
                success_count = len(results['success'])
                duplicate_count = len(results['duplicates'])
                
                if success_count > 0:
                    flash(f'{success_count} URL(s) added successfully!', 'success')
                if duplicate_count > 0:
                    flash(f'{duplicate_count} duplicate URL(s) skipped', 'warning')
                if error_list:
                    for error in error_list[:5]:  # Limit displayed errors
                        flash(error, 'error')
                
                if success_count > 0:
                    return redirect(url_for('admin.dashboard'))
            else:
                # Show validation errors
                for error in error_list:
                    flash(error, 'error')
        
        # Single mode: one URL (backward compatibility)
        else:
            # Validate data
            is_valid, errors = validate_url_data(request.form)
            
            if is_valid:
                # Prepare and save data
                url_data = prepare_url_data(request.form)
                result = url_repo.create(url_data)
                
                if result:
                    flash('URL added successfully!', 'success')
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash('This URL already exists', 'error')
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
        # Validate data
        is_valid, errors = validate_url_data(request.form)
        
        if is_valid:
            # Prepare and update data
            url_data = prepare_url_data(request.form)
            success = url_repo.update(url_id, url_data)
            
            if success:
                flash('URL updated successfully!', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Failed to update URL', 'error')
        else:
            # Show validation errors
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
