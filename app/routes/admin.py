from flask import Blueprint, render_template, request, redirect, url_for
from app.services import database, case_study_manager
from app.routes.auth import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_views': database.get_total_views(),
        'unique_visitors': database.get_unique_visitors(),
        'top_pages': database.get_top_pages()
    }
    return render_template('dashboard.html', stats=stats)

@admin_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_case_study():
    if request.method == 'POST':
        title = request.form.get('title')
        tags = request.form.get('tags')
        challenge = request.form.get('challenge')
        solution = request.form.get('solution')
        impact = request.form.get('impact')
        content = request.form.get('content')
        
        case_study_manager.save_case_study(title, tags, challenge, solution, impact, content)
        return redirect(url_for('main.case_studies_page'))
        
    return render_template('create-case-study.html')
