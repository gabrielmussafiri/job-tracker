from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

#load .env file
load_dotenv()

# Initialize extension
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app,db)
    CORS(app)
    
    #IMport models so flask Knows the table
    from app.models import User, Job , Note
    
    #Register routes
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)

    return app