from flask import Blueprint, render_template, request, Response, url_for
from app.services import case_study_manager, database

main_bp = Blueprint('main', __name__)

from app.utils import get_client_ip

@main_bp.before_app_request
def track_views():
    # Track unique visitor
    database.track_visitor(get_client_ip())
    
    if request.endpoint in ['main.index', 'main.case_studies_page']:
        database.increment_view(request.path)

@main_bp.route('/')
def index():
    case_studies = case_study_manager.get_all_case_studies()
    return render_template('index.html', case_studies=case_studies)

@main_bp.route('/case-studies')
def case_studies_page():
    case_studies = case_study_manager.get_all_case_studies()
    return render_template('case-studies.html', case_studies=case_studies)

@main_bp.route('/case-study/<id>')
def case_study_detail(id):
    case_study = case_study_manager.get_case_study_by_id(id)
    if not case_study:
        return render_template('404.html'), 404
    return render_template('case-study-detail.html', case_study=case_study)

@main_bp.route('/sitemap.xml')
def sitemap():
    case_studies = case_study_manager.get_all_case_studies()
    xml = render_template('sitemap.xml', posts=case_studies)
    return Response(xml, mimetype='application/xml')

@main_bp.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /admin/\nSitemap: " + url_for('main.sitemap', _external=True)
