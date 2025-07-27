from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate  # Import Migrate

from models import db  # Use the shared db instance from __init__.py
from dotenv import load_dotenv
import os
import openai


load_dotenv()  # Load environment variables from .env

# Now you can access it like this
openai.api_key = os.getenv("OPENAI_API_KEY")


# Create the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and login manager
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

migrate = Migrate(app, db)  # Add this line to initialize migration

# Import User model for login manager
from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints (routes)
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.planner import planner_bp
from routes.reminders import reminders_bp
from routes.admin import admin_bp
from routes.home import home_bp  # NEW - Home blueprint

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(planner_bp)
app.register_blueprint(reminders_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(home_bp)  # NEW - Register home blueprint

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
