from flask import Flask, render_template
import os

from index.index import index_bp, fetch_docs
from projects.projects import projects_bp, fetch_projects

app = Flask(__name__)

app.register_blueprint(index_bp, url_prefix='/')
app.register_blueprint(projects_bp, url_prefix='/projects')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('/404.html', intro=False)

@app.errorhandler(500)
def server_error(e):
	return render_template('/500.html', title="500 Error", intro=False)

@app.route('/maintenance')
def maintenance():
	return render_template('/maintenance.html', title="Maintenance", intro=False)

@app.route('/refresh')
def refresh():
	fetch_docs()
	fetch_projects()
	return 'Database Refreshed!'

def create_app():
	refresh()
	return app