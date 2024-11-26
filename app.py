from flask import Flask
from flask_sqlalchemy import SQLAlchemy

audit_trail_db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audit_trail.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    audit_trail_db.init_app(app) 
    
    with app.app_context():
        from . import routes 
        audit_trail_db.create_all()
        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    