from models import db

class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    remind_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.id'), nullable=True)  # Link to StudyPlan

   
