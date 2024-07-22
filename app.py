from flask import Flask, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__,template_folder='templates')
app.secret_key = 'Pass@123'  # Replace with your secret key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'portal_user'
app.config['MYSQL_PASSWORD'] = 'BenchSharing@123'
app.config['MYSQL_DB'] = 'bench_sharing_portal'

mysql = MySQL(app)
app.config['MYSQL']=mysql

from routes.user_routes import user_bp
#from routes.admin_routes import admin_bp

from routes.user_routes import company_bp

app.register_blueprint(user_bp)
app.register_blueprint(company_bp, url_prefix='/company')
#app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if 'username' in session and session['user_type'] == 'admin':
        return render_template('admin_dashboard.html', username=session['username'])
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('user.login'))

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     session.pop('user_type', None)
#     return redirect(url_for('user.login'))

# if __name__ == '__main__':
#     app.run(debug=True)
