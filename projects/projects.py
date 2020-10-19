from flask import Blueprint, render_template
from airtable import Airtable
import os

projects_bp = Blueprint('projects_bp', __name__,
	template_folder='templates',
	static_folder='static')

AIRTABLE_API = os.environ.get('AIRTABLE_API')
project_engine = Airtable('appPtZ9HagmI97ixP', 'Projects', AIRTABLE_API)
projects = None

def fetch_projects():
	data = []
	for row in project_engine.get_all():
		temp = {}
		row = row['fields']
		for category in ['Id', 'Title', 'Subtitle', 'URL', 'Explanation', 'Project_available', 'Code_available', 'Button', 'Github', 'Thumbnail']:
			try:
				if category == "Thumbnail":
					temp['Thumbnail'] = row['Thumbnail'][0]['url']
				else:
					temp[category] = row[category]
			except:
				pass	
		data.append(temp)
	global projects
	projects = sorted(list(filter(None, data)), key=lambda k: k['Id'])

@projects_bp.route('/')
def index():
	global projects
	return render_template(
		'projects/index.html', 
		title='Projects - Jaeyoung Cho', 
		intro=False, 
		projects=reversed(projects),
		menu_projects=True
		)


