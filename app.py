from flask import Flask, render_template
from models import Resource, db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Secret key for session management
    app.config['SECRET_KEY'] = 'pass@123'  # Replace with a strong, unique key

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register Blueprints
    from routes.user_routes import user_bp
    from routes.resource_routes import resource_bp

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(resource_bp, url_prefix='/resource')

    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/dashboard')
    def dashboard():
        resources = Resource.query.all()  # Fetch all resources from the database
        return render_template('dashboard.html', resources=resources)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
