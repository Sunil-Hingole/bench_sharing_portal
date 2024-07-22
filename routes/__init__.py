from flask import Flask, render_template
from flask_mysqldb import MySQL
from routes.resource_routes import resource_bp

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'portal_user'
app.config['MYSQL_PASSWORD'] = 'BenchSharing@123'
app.config['MYSQL_DB'] = 'bench_sharing_portal'

mysql = MySQL(app)

app.register_blueprint(resource_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
