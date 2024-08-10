# from flask import Flask
# from models import db
# from routes.user_routes import user_bp
# from routes.resource_routes import resource_bp  # Adjust the import path based on your file structure

# def create_app():
#     app = Flask(__name__)

#     # App configuration
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     # Initialize the SQLAlchemy instance with the app
#     db.init_app(app)

#     # Register Blueprints
#     app.register_blueprint(user_bp)
#     app.register_blueprint(resource_bp)

#     return app
