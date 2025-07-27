import os
import sys

# Add root directory (StudySync/) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from config import Config
from models import db
from models.user import User
from models.study_plan import StudyPlan
from models.reminders import Reminder

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully.")
