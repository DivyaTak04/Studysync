from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.study_plan import StudyPlan
from models import db
from datetime import datetime

planner_bp = Blueprint('planner', __name__, url_prefix='/planner')

@planner_bp.route('/', methods=['GET', 'POST'])
@login_required
def planner():
    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form.get('description') or "No description"

        
       
        status = request.form.get('status', 'pending')  # Default to 'pending'
        priority = request.form.get('priority', 'normal')  # Default to 'normal'
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        # Convert start_time and end_time to datetime objects
        start_time_obj = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time_obj = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

        # Create the new study plan
        new_plan = StudyPlan(
            subject=subject,
            description=description,
            
            
            status=status,
            priority=priority,
            start_time=start_time_obj,
            end_time=end_time_obj,
            user_id=current_user.id
        )
        db.session.add(new_plan)
        db.session.commit()
        return redirect(url_for('planner.planner'))

    # Get the study plans for the current user, ordered by the date
    plans = StudyPlan.query.filter_by(user_id=current_user.id).order_by(StudyPlan.created_at).all()

    return render_template('planner.html', plans=plans)

# 🔄 Dummy AI Suggestion Route for Computer Science subjects
@planner_bp.route('/suggest', methods=['GET'])
@login_required
def suggest_topics():
    subject = request.args.get('subject', '').strip().lower()
    if not subject:
        return jsonify({'success': False, 'error': 'No subject provided.'})

    # Simulated AI suggestions
    dummy_suggestions = {
        'python': [
            "Variables and Data Types",
            "Control Flow (if, for, while)",
            "Functions and Modules",
            "Object-Oriented Programming",
            "File Handling"
        ],
        'data structures': [
            "Arrays and Lists",
            "Stacks and Queues",
            "Trees and Graphs",
            "Hash Tables",
            "Recursion"
        ],
        'dbms': [
            "ER Diagrams",
            "SQL Queries",
            "Normalization",
            "Transactions and Concurrency",
            "Indexing"
        ],
        'os': [
            "Process Management",
            "Memory Management",
            "File Systems",
            "CPU Scheduling",
            "Deadlocks"
        ],
        'computer networks': [
            "OSI Model",
            "TCP/IP Protocol",
            "Routing and Switching",
            "Network Security",
            "IP Addressing"
        ],
        'ai': [
            "Introduction to AI",
            "Search Algorithms",
            "Machine Learning Basics",
            "Natural Language Processing",
            "Neural Networks"
        ]
    }

    # Fallback generic suggestions if subject not matched
    suggestions = dummy_suggestions.get(subject, [
        f"Important topic 1 in {subject.title()}",
        f"Important topic 2 in {subject.title()}",
        f"Important topic 3 in {subject.title()}",
        f"Important topic 4 in {subject.title()}",
        f"Important topic 5 in {subject.title()}"
    ])

    return jsonify({'success': True, 'suggestions': suggestions})

@planner_bp.route('/delete/<int:plan_id>', methods=['POST'])
@login_required
def delete_plan(plan_id):
    plan = StudyPlan.query.filter_by(id=plan_id, user_id=current_user.id).first()
    if plan:
        db.session.delete(plan)
        db.session.commit()
    return redirect(url_for('planner.planner'))
