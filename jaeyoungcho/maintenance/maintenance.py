from flask import Blueprint, render_template

maintenance_bp = Blueprint('maintenance_bp', __name__)

@maintenance_bp.route('/')
def maintenance():
    return render_template('/maintenance.html', title="Maintenance", intro=False)


