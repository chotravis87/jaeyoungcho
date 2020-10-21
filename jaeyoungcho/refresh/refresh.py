from flask import Blueprint, redirect

refresh_bp = Blueprint('refresh_bp', __name__)

@refresh_bp.route('/', methods=['POST'])
def refresh():
    from ..index.index import docs_fetcher
    from ..projects.projects import project_fetcher
    docs_fetcher.update()
    project_fetcher.update()
    return "true"