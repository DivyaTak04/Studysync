from flask_login import UserMixin
from models import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    study_plans = db.relationship('StudyPlan', backref='user', lazy=True)
    reminders = db.relationship('Reminder', backref='user', lazy=True)
