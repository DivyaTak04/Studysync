# from models import db

# class StudyPlan(db.Model):
#     __tablename__ = 'study_plans'

#     id = db.Column(db.Integer, primary_key=True)
#     subject = db.Column(db.String(100), nullable=False)
#     topic = db.Column(db.String(200), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     time = db.Column(db.Time, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    
# models/study_plan.py

from models import db
from datetime import datetime

class StudyPlan(db.Model):
    __tablename__ = 'study_plans'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Auto add
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Auto update
    status = db.Column(db.String(20), default='pending')  # Could be 'pending', 'in_progress', 'completed'
    priority = db.Column(db.String(10), default='normal')  # Could be 'low', 'normal', 'high'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with the Reminder model
    reminders = db.relationship('Reminder', backref='study_plan_ref', lazy=True)

    def __repr__(self):
        return f"<StudyPlan {self.subject} - {self.status}>"

