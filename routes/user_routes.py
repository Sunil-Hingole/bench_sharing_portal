# routes/user_routes.py
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Resource, db
from models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        user = User(username=username, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username
            session['user_type'] = user.user_type
            if user.user_type == 'admin':
                return redirect(url_for('resource.dashboard'))
            elif user.user_type == 'company':
                return redirect(url_for('resource.company_dashboard'))
        flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('user.login'))

@user_bp.route('/dashboard')
def dashboard():
    # Define the dashboard view
    return render_template('dashboard.html')


@user_bp.route('/booked_resources')
def booked_resources():
    username = session.get('username')
    booked_resources = Resource.query.filter_by(booked_by=username).all()
    return render_template('booked_resources.html', resources=booked_resources)



@user_bp.route('/update_resource/<int:id>', methods=['GET', 'POST'])
def update_resource(id):
    resource = Resource.query.get_or_404(id)
    
    if request.method == 'POST':
        resource.name = request.form['name']
        resource.description = request.form['description']
        
        # Convert the string dates to datetime objects
        try:
            resource.available_from = datetime.strptime(request.form['available_from'], '%Y-%m-%dT%H:%M')
            resource.booked_by = request.form['booked_by']
            resource.booked_at = datetime.strptime(request.form['booked_at'], '%Y-%m-%dT%H:%M') if request.form['booked_at'] else None
        except ValueError as e:
            flash(f"Invalid date format: {e}", 'danger')
            return redirect(url_for('user.update_resource', id=id))
        
        db.session.commit()
        flash('Resource updated successfully!', 'success')
        return redirect(url_for('resource.dashboard'))
    
    return render_template('update_resource.html', resource=resource)


@user_bp.route('/add_booked_resource', methods=['GET', 'POST'])
def add_booked_resource():
    if request.method == 'POST':
        resource_id = request.form['resource_id']
        booked_by = session.get('username')
        booked_at = request.form['booked_at']
        available_from = request.form['available_from']
        
        # Find the resource by ID
        resource = Resource.query.get(resource_id)
        if resource:
            resource.booked_by = booked_by
            resource.booked_at = datetime.strptime(booked_at, '%Y-%m-%dT%H:%M')
            resource.available_from = datetime.strptime(available_from, '%Y-%m-%d')
            db.session.commit()
            flash('Resource booked successfully!')
            return redirect(url_for('user.booked_resources'))
        else:
            flash('Resource not found.')
    
    # For GET request, display the form
    resources = Resource.query.filter(Resource.booked_by.is_(None)).all()  # Get resources that are not booked
    return render_template('add_booked_resource.html', resources=resources)


@user_bp.route('/company_dashboard')
def company_dashboard():
    if 'username' not in session or session.get('user_type') != 'company':
        return redirect(url_for('user.login'))
    
    # Fetch all resources
    resources = Resource.query.all()
    return render_template('user.company_dashboard.html', resources=resources)