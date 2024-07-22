from flask import Blueprint, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

resource_bp = Blueprint('resource_bp', __name__)

@resource_bp.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        # Logic to add resource
        pass
    # Logic to display resources
    return render_template('resources.html')
