from flask import Flask, render_template, Blueprint

# Custom Error Page
def page_not_found(e):
	return render_template('/404.html', intro=False)

def server_error(e):
	return render_template('/500.html', title="500 Error", intro=False)

projects_bp = Blueprint('projects_bp', __name__)

# Initialize
def create_app():
    from .index.index import index_bp, chatbot
    from .projects.projects import projects_bp
    from .maintenance.maintenance import maintenance_bp

    app = Flask(__name__)

    app.register_blueprint(index_bp, url_prefix='/')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(maintenance_bp, url_prefix='/maintenance')


    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    return app
