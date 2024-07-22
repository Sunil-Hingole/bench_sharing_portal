# from flask import Blueprint, render_template, request, session, current_app
# from models.resource import Resource

# company_bp = Blueprint('company', __name__)

# @company_bp.route('/dashboard')
# def dashboard():
#     cursor = current_app.config['MYSQL'].connection.cursor()
#     cursor.execute('''
#         SELECT rt.name AS resource_type, COUNT(r.id) AS count
#         FROM resources r
#         JOIN resource_types rt ON r.resource_type_id = rt.id
#         WHERE r.booked_by IS NULL
#         GROUP BY rt.name
#     ''')
#     resources_by_type = cursor.fetchall()
#     cursor.close()
#     return render_template('company_dashboard.html', resources_by_type=resources_by_type)

# @company_bp.route('/resources/<resource_type>')
# def resources(resource_type):
#     cursor = current_app.config['MYSQL'].connection.cursor()
#     cursor.execute('''
#         SELECT r.id, r.name, r.description, r.available_from
#         FROM resources r
#         JOIN resource_types rt ON r.resource_type_id = rt.id
#         WHERE rt.name = %s AND r.booked_by IS NULL
#     ''', (resource_type,))
#     resources = cursor.fetchall()
#     cursor.close()
#     return render_template('resources.html', resources=resources, resource_type=resource_type)

# @company_bp.route('/book/<int:resource_id>')
# def book(resource_id):
#     user_id = session.get('user_id')
#     if user_id:
#         cursor = current_app.config['MYSQL'].connection.cursor()
#         cursor.execute('''
#             UPDATE resources
#             SET booked_by = %s, booked_at = NOW()
#             WHERE id = %s
#         ''', (user_id, resource_id))
#         current_app.config['MYSQL'].connection.commit()
#         cursor.close()
#     return redirect(url_for('company.dashboard'))

# @company_bp.route('/my_bookings')
# def my_bookings():
#     user_id = session.get('user_id')
#     if user_id:
#         cursor = current_app.config['MYSQL'].connection.cursor()
#         cursor.execute('''
#             SELECT r.id, r.name, rt.name AS resource_type, r.description, r.available_from
#             FROM resources r
#             JOIN resource_types rt ON r.resource_type_id = rt.id
#             WHERE r.booked_by = %s
#         ''', (user_id,))
#         bookings = cursor.fetchall()
#         cursor.close()
#         return render_template('my_bookings.html', bookings=bookings)
#     return redirect(url_for('user.login'))

# @company_bp.route('/release/<int:resource_id>')
# def release(resource_id):
#     user_id = session.get('user_id')
#     if user_id:
#         cursor = current_app.config['MYSQL'].connection.cursor()
#         cursor.execute('''
#             UPDATE resources
#             SET booked_by = NULL, booked_at = NULL
#             WHERE id = %s AND booked_by = %s
#         ''', (resource_id, user_id))
#         current_app.config['MYSQL'].connection.commit()
#         cursor.close()
#     return redirect(url_for('company.my_bookings'))
