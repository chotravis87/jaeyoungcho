from flask import Blueprint, render_template

from ..database import Database

projects_bp = Blueprint('projects_bp', __name__,
	template_folder='templates',
	static_folder='static')

project_fetcher = Database('appPtZ9HagmI97ixP', 'Projects')

@projects_bp.route('/')
def index():
	global project_fetcher
	projects = project_fetcher.fetch(['Id', 'Title', 'Subtitle', 'URL', 'Explanation', 'Project_available', 'Code_available', 'Button', 'Github', 'Thumbnail'], 'Id')
	return render_template(
		'projects/index.html', 
		title='Projects - Jaeyoung Cho', 
		intro=False, 
		projects=reversed(projects),
		menu_projects=True
		)


