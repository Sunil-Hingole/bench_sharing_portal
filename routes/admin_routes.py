# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from models import Resource, ResourceType

# admin_bp = Blueprint('admin', __name__)

# @admin_bp.route('/admin/dashboard')
# def admin_dashboard():
#     if 'username' in session and session['user_type'] == 'admin':
#         resources = Resource.query.all()
#         return render_template('admin_dashboard.html', resources=resources)
#     else:
#         flash('You are not authorized to access this page.')
#         return redirect(url_for('user.login'))

# @admin_bp.route('/create', methods=['GET', 'POST'])
# def create_resource():
#     if request.method == 'GET':
#         resource_types = ResourceType.query.all()
#         return render_template('create.html', resource_types=resource_types)
#     elif request.method == 'POST':
#         name = request.form['name']
#         resource_type_id = request.form['resource_type_id']
#         description = request.form['description']
#         resource = Resource(name=name, resource_type_id=resource_type_id, description=description)
#         db.session.add(resource)
#         db.session.commit()
#         flash('Resource created successfully')
#         return redirect(url_for('admin.admin_dashboard'))

# @admin_bp.route('/edit/<int:resource_id>', methods=['GET', 'POST'])
# def edit_resource(resource_id):
#     resource = Resource.query.get_or_404(resource_id)
#     if request.method == 'GET':
#         resource_types = ResourceType.query.all()
#         return render_template('edit.html', resource=resource, resource_types=resource_types)
#     elif request.method == 'POST':
#         resource.name = request.form['name']
#         resource.resource_type_id = request.form['resource_type_id']
#         resource.description = request.form['description']
#         db.session.commit()
#         flash('Resource updated successfully')
#         return redirect(url_for('admin.admin_dashboard'))

# @admin_bp.route('/delete/<int:resource_id>', methods=['GET', 'POST'])
# def delete_resource(resource_id):
#     resource = Resource.query.get_or_404(resource_id)
#     if request.method == 'GET':
#         return render_template('delete.html', resource=resource)
#     elif request.method == 'POST':
#         db.session.delete(resource)
#         db.session.commit()
#         flash('Resource deleted successfully')
#         return redirect(url_for('admin.admin_dashboard'))