from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.user import User
from models.study_plan import StudyPlan
from models.reminders import Reminder

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_dashboard():
    # Optional: Restrict access to only specific users (e.g., admin username)
    if current_user.username != 'admin':
        return "Access Denied", 403

    users = User.query.all()
    plans = StudyPlan.query.all()
    reminders = Reminder.query.all()

    return render_template('admin.html', users=users, plans=plans, reminders=reminders)
