# routes/resource_routes.py
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from models import db
from models.resource import Resource, ResourceType
from models.user import User


resource_bp = Blueprint('resource', __name__)

@resource_bp.route('/add', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        name = request.form['name']
        resource_type_id = request.form['resoursetypeid']
        description = request.form['description']
        available_from = request.form['available_from']
        category = request.form.get('category')
        booked_by = request.form.get('booked_by')
        booked_at = request.form.get('booked_at')

        new_resource = Resource(
            name=name,
            resource_type_id=resource_type_id,
            description=description,
            available_from=available_from,
            category=category,
            booked_by=booked_by,
            booked_at=booked_at
        )
        
        db.session.add(new_resource)
        db.session.commit()
        
        flash('Resource added successfully!')
        return redirect(url_for('resource.dashboard'))
    
    resource_types = ResourceType.query.all()
    return render_template('add.html', resource_types=resource_types)

@resource_bp.route('/dashboard')
def dashboard():
    resources = Resource.query.all()
    return render_template('dashboard.html', resources=resources)

from datetime import datetime

@resource_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_resource(id):
    resource = Resource.query.get_or_404(id)
    
    if request.method == 'POST':
        resource.name = request.form.get('name', resource.name)
        
        # Convert string dates to datetime objects
        available_from_str = request.form.get('available_from')
        booked_at_str = request.form.get('booked_at')
        
        if available_from_str:
            try:
                resource.available_from = datetime.fromisoformat(available_from_str)
            except ValueError:
                flash('Invalid date format for available_from.')
                return redirect(url_for('resource.update_resource', id=id))

        if booked_at_str:
            try:
                resource.booked_at = datetime.fromisoformat(booked_at_str)
            except ValueError:
                flash('Invalid date format for booked_at.')
                return redirect(url_for('resource.update_resource', id=id))
        
        resource.booked_by = request.form.get('booked_by', resource.booked_by)

        db.session.commit()
        flash('Resource updated successfully!')
        return redirect(url_for('resource.dashboard'))
    
    resource_types = ResourceType.query.all()
    return render_template('update.html', resource=resource, resource_types=resource_types)

@resource_bp.route('/delete/<int:id>', methods=['POST'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted successfully!')
    return redirect(url_for('resource.dashboard'))


@resource_bp.route('/company_dashboard')
def company_dashboard():
    if 'username' not in session or session.get('user_type') != 'company':
        return redirect(url_for('user.login'))
    
    # Fetch all resources
    resources = Resource.query.all()
    return render_template('company_dashboard.html', resources=resources)


@resource_bp.route('/bench_resources/<category>', methods=['GET', 'POST'])
def bench_resources(category):
    # Fetch resources of the given category
    resources = Resource.query.filter_by(category=category, available=True).all()

    if request.method == 'POST':
        resource_id = request.form['resource_id']
        resource = Resource.query.get(resource_id)
        if resource and resource.available:
            resource.booked_by = session['username']
            resource.available = False
            db.session.commit()
            flash('Resource booked successfully!')
        else:
            flash('Failed to book resource.')
        return redirect(url_for('resource.bench_resources', category=category))

    return render_template('bench_resources.html', resources=resources, category=category)

@resource_bp.route('/booked_resources')
def booked_resources():
    # Fetch resources booked by the logged-in user
    username = session.get('username')
    resources = Resource.query.filter_by(booked_by=username).all()
    return render_template('booked_resources.html', resources=resources)
