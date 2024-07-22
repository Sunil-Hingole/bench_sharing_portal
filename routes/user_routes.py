from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.resource import Resource
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

user_bp = Blueprint('user', __name__)
company_bp = Blueprint('company', __name__)

class UpdateResourceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    resoursetypeid = StringField('Resource Type ID', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    available_from = StringField('Available From', validators=[DataRequired()])
    booked_by = StringField('Booked By', validators=[DataRequired()])
    booked_at = StringField('Booked At', validators=[DataRequired()])
    submit = SubmitField('Update Resource')

class DeleteResourceForm(FlaskForm):
    pass

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user_type = request.form['user_type']
        user = User(username, password, user_type)
        user.save_to_db(current_app.config['MYSQL'])
        return redirect(url_for('user.login'))
    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = User.get_by_username(current_app.config['MYSQL'], username)
        if user_data:
            print("User found:", user_data)
            if check_password_hash(user_data[2], password):
                print("Password correct")
                session['username'] = user_data[1]
                session['user_type'] = user_data[3]
                print("Session username:", session['username'])
                print("Session user type:", session['user_type'])
                if session['user_type'] == 'admin':
                    return redirect(url_for('user.dashboard'))
                elif session['user_type'] == 'company':
                    print("Redirecting to company dashboard")
                    return redirect(url_for('user.company_dashboard'))
            else:
                print("Password incorrect")
        else:
            print("User not found")
    print("Login failed, redirecting to login page")
    return render_template('login.html')

@user_bp.route('/company_dashboard')
def company_dashboard():
    engineers_count = get_count_for_category('engineers')
    seating_space_count = get_count_for_category('seating_space')
    product_licenses_count = get_count_for_category('product_licenses')

    return render_template(
        'company_dashboard.html',
        engineers_count=engineers_count,
        seating_space_count=seating_space_count,
        product_licenses_count=product_licenses_count
    )

def get_count_for_category(category):
    # Implement your logic to fetch the count from the database
    pass

@company_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        resoursetypeid = request.form['resoursetypeid']
        description = request.form['description']
        available_from = request.form['available_from']
        booked_by = request.form['booked_by']  # Use get() to handle optional fields
        booked_at = request.form['booked_at']
        
        resource = Resource(name, resoursetypeid, description, available_from, booked_by, booked_at)
        resource.save_to_db(current_app.config['MYSQL'])  # Assuming you have a save_to_db method
        return redirect(url_for('user.dashboard'))  # Adjust view_resources to the correct route
    
    return render_template('add.html')

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('user.login'))

@user_bp.route('/dashboard')
def dashboard():
    try:
        cursor = current_app.config['MYSQL'].connection.cursor()

        # Fetch resource records with specific columns
        cursor.execute('''
            SELECT r.name, r.resource_type_id, r.description, r.available_from, u.username AS booked_by, r.booked_at
            FROM resources r
            LEFT JOIN users u ON r.booked_by = u.id
        ''')
        resources = cursor.fetchall()
        print("Resources by Type:", resources)  # Debug print

        cursor.close()

        return render_template('dashboard.html', allresources=resources)

    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return render_template('add.html')

@user_bp.route('/update/<string:resource_name>', methods=['GET', 'POST'])
def update_resource(resource_name):
    form = UpdateResourceForm()
    if request.method == 'POST':
        # Update resource logic here
        name = request.form['name']
        resoursetypeid = request.form['resoursetypeid']
        description = request.form['description']
        available_from = request.form['available_from']
        booked_by = request.form['booked_by']
        booked_at = request.form['booked_at']

        # Update resource in database
        cursor = current_app.config['MYSQL'].connection.cursor()
        cursor.execute('''
            UPDATE resources
            SET name = %s, resource_type_id = %s, description = %s, available_from = %s, booked_by = %s, booked_at = %s
            WHERE name = %s
        ''', (name, resoursetypeid, description, available_from, booked_by, booked_at, resource_name))
        cursor.close()

        return redirect(url_for('user.dashboard'))

    # Fetch resource data for update form
    cursor = current_app.config['MYSQL'].connection.cursor()
    cursor.execute('SELECT * FROM resources WHERE name = %s', (resource_name,))
    resource_data = cursor.fetchone()
    cursor.close()

    if resource_data is None:
        flash('Resource not found')
        return redirect(url_for('user.dashboard'))

    return render_template('update.html', form=form, resource_data=resource_data)


@user_bp.route('/delete/<string:resource_name>', methods=['GET', 'POST'])
def delete_resource(resource_name):
    if request.method == 'GET':
        cursor = current_app.config['MYSQL'].connection.cursor()
        cursor.execute('SELECT * FROM resources WHERE name = %s', (resource_name,))
        resource_data = cursor.fetchone()
        cursor.close()

        if resource_data is None:
            flash('Resource not found')
            return redirect(url_for('user.dashboard'))

        return render_template('delete.html', resource_data=resource_data)

    elif request.method == 'POST':
        cursor = current_app.config['MYSQL'].connection.cursor()
        cursor.execute('DELETE FROM resources WHERE name = %s', (resource_name,))
        current_app.config['MYSQL'].connection.commit()
        cursor.close()
        flash('Resource deleted successfully')
        return redirect(url_for('user.dashboard'))