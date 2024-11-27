"""
This module initializes the app.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

audit_trail_db = SQLAlchemy()

def create_app():
    """
    Create and configure an instance of the Flask application. This function sets up the Flask
    app with the given configuration, initializes the database, registers blueprints,
    and creates the necessary database tables.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audit_trail.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    audit_trail_db.init_app(app)

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)
        audit_trail_db.create_all()
        return app
