# from flask import Blueprint, render_template, redirect, url_for, request, flash
# from flask_login import login_required, current_user
# from models.reminders import Reminder
# from models.study_plan import StudyPlan
# from models import db
# from datetime import datetime

# reminders_bp = Blueprint('reminders', __name__)

# @reminders_bp.route('/reminders', methods=['GET', 'POST'])
# @login_required
# def reminders():
#     if request.method == 'POST':
#         message = request.form['message']
#         remind_at = request.form['remind_at']
#         study_plan_id = request.form.get('study_plan_id') or None

#         try:
#             remind_at = datetime.strptime(remind_at, '%Y-%m-%dT%H:%M')
#             reminder = Reminder(
#                 message=message,
#                 remind_at=remind_at,
#                 user_id=current_user.id,
#                 study_plan_id=study_plan_id if study_plan_id else None
#             )
#             db.session.add(reminder)
#             db.session.commit()
#             flash('Reminder set successfully!', 'success')
#         except Exception as e:
#             flash('Invalid date/time format.', 'danger')

#         return redirect(url_for('reminders.reminders'))

#     reminder_objs = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.remind_at).all()
    
#     reminders = [
#         {
#             'id': r.id,
#             'message': r.message,
#             'remind_at': r.remind_at.isoformat(),
#             'linked_plan': r.study_plan_ref.subject if r.study_plan_ref else None
#         }
#         for r in reminder_objs
#     ]

#     user_plans = StudyPlan.query.filter_by(user_id=current_user.id).all()

#     return render_template('reminders.html', reminders=reminders, reminder_objs=reminder_objs, user_plans=user_plans)
# In reminders.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models.reminders import Reminder
from models.study_plan import StudyPlan
from models import db
from datetime import datetime

reminders_bp = Blueprint('reminders', __name__)

# AI-driven dummy function to suggest reminders based on study plan subject
def ai_reminder_suggestions(subject):
    # Simulated AI suggestions for reminders
    suggestions = {
        'python': [
            "Review Python concepts like loops and functions",
            "Practice coding challenges on variables",
            "Set a reminder to revisit object-oriented concepts"
        ],
        'data structures': [
            "Revise binary trees and graphs",
            "Review sorting algorithms",
            "Practice dynamic programming problems"
        ],
        'dbms': [
            "Study SQL queries and joins",
            "Revise normalization and ER diagrams",
            "Complete DBMS assignments"
        ],
        'os': [
            "Review memory management in operating systems",
            "Study CPU scheduling algorithms",
            "Complete your OS lab exercises"
        ]
    }
    
    # Return suggestions based on subject
    return suggestions.get(subject.lower(), ["Start working on your next topic!"])

@reminders_bp.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    if request.method == 'POST':
        message = request.form['message']
        remind_at = request.form['remind_at']
        study_plan_id = request.form.get('study_plan_id') or None

        try:
            remind_at = datetime.strptime(remind_at, '%Y-%m-%dT%H:%M')

            # AI-driven reminder suggestion
            study_plan = StudyPlan.query.filter_by(id=study_plan_id, user_id=current_user.id).first()
            if study_plan:
                ai_suggestions = ai_reminder_suggestions(study_plan.subject)
                message = ai_suggestions[0]  # Set the first AI suggestion as the default message

            reminder = Reminder(
                message=message,
                remind_at=remind_at,
                user_id=current_user.id,
                study_plan_id=study_plan_id if study_plan_id else None
            )
            db.session.add(reminder)
            db.session.commit()
            flash('Reminder set successfully!', 'success')
        except Exception as e:
            flash(f'Error setting reminder: {e}', 'danger')

        return redirect(url_for('reminders.reminders'))

    reminder_objs = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.remind_at).all()
    
    reminders = [
        {
            'id': r.id,
            'message': r.message,
            'remind_at': r.remind_at.isoformat(),
            'linked_plan': r.study_plan_ref.subject if r.study_plan_ref else None
        }
        for r in reminder_objs
    ]

    user_plans = StudyPlan.query.filter_by(user_id=current_user.id).all()

    return render_template('reminders.html', reminders=reminders, reminder_objs=reminder_objs, user_plans=user_plans)
