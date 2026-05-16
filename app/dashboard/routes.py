from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Project, Task, User, ProjectMember

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin():
        projects = Project.query.order_by(Project.created_at.desc()).all()
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        users = User.query.all()
        overdue = [task for task in tasks if task.is_overdue()]
        return render_template(
            "dashboard/admin_dashboard.html",
            projects=projects,
            tasks=tasks,
            users=users,
            overdue=overdue
        )

    memberships = ProjectMember.query.filter_by(user_id=current_user.id).all()
    project_ids = [m.project_id for m in memberships]
    projects = Project.query.filter(Project.id.in_(project_ids)).all() if project_ids else []
    tasks = Task.query.filter_by(assigned_to=current_user.id).order_by(Task.created_at.desc()).all()
    overdue = [task for task in tasks if task.is_overdue()]
    return render_template(
        "dashboard/member_dashboard.html",
        projects=projects,
        tasks=tasks,
        overdue=overdue
    )
