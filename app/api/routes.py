from functools import wraps

from flask import jsonify, request
from flask_login import current_user, login_required

from app import db
from app.api import api_bp
from app.models import Project, ProjectMember, Task, User


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({"error": "Admin access required"}), 403
        return func(*args, **kwargs)

    return wrapper


def serialize_project(project):
    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "deadline": project.deadline,
        "created_by": project.created_by,
        "progress": project.progress(),
        "task_count": len(project.tasks),
    }


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "project_id": task.project_id,
        "project": task.project.title,
        "assigned_to": task.assigned_to,
        "assignee": task.assignee.name,
        "created_by": task.created_by,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "is_overdue": task.is_overdue(),
    }


def require_fields(data, fields):
    missing = [field for field in fields if not data.get(field)]
    if missing:
        return jsonify({"error": "Missing required fields", "fields": missing}), 400
    return None


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.get("/dashboard")
@login_required
def dashboard_summary():
    if current_user.is_admin():
        projects = Project.query.all()
        tasks = Task.query.all()
        users_count = User.query.count()
    else:
        memberships = ProjectMember.query.filter_by(user_id=current_user.id).all()
        project_ids = [membership.project_id for membership in memberships]
        projects = Project.query.filter(Project.id.in_(project_ids)).all() if project_ids else []
        tasks = Task.query.filter_by(assigned_to=current_user.id).all()
        users_count = None

    return jsonify(
        {
            "projects": len(projects),
            "tasks": len(tasks),
            "overdue": len([task for task in tasks if task.is_overdue()]),
            "completed": len([task for task in tasks if task.status == "Completed"]),
            "users": users_count,
        }
    )


@api_bp.get("/projects")
@login_required
def list_projects():
    if current_user.is_admin():
        projects = Project.query.order_by(Project.created_at.desc()).all()
    else:
        memberships = ProjectMember.query.filter_by(user_id=current_user.id).all()
        project_ids = [membership.project_id for membership in memberships]
        projects = Project.query.filter(Project.id.in_(project_ids)).all() if project_ids else []

    return jsonify([serialize_project(project) for project in projects])


@api_bp.post("/projects")
@login_required
@admin_required
def create_project():
    data = request.get_json(silent=True) or {}
    validation = require_fields(data, ["title", "description", "deadline"])
    if validation:
        return validation

    project = Project(
        title=data["title"].strip(),
        description=data["description"].strip(),
        deadline=data["deadline"],
        created_by=current_user.id,
    )
    db.session.add(project)
    db.session.commit()
    db.session.add(ProjectMember(project_id=project.id, user_id=current_user.id, role="admin"))
    db.session.commit()
    return jsonify(serialize_project(project)), 201


@api_bp.get("/projects/<int:project_id>")
@login_required
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    if not current_user.is_admin():
        membership = ProjectMember.query.filter_by(project_id=project.id, user_id=current_user.id).first()
        if not membership:
            return jsonify({"error": "You are not a member of this project"}), 403
    return jsonify(serialize_project(project))


@api_bp.get("/tasks")
@login_required
def list_tasks():
    status = request.args.get("status")
    query = Task.query
    if not current_user.is_admin():
        query = query.filter_by(assigned_to=current_user.id)
    if status:
        query = query.filter_by(status=status)

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([serialize_task(task) for task in tasks])


@api_bp.post("/tasks")
@login_required
@admin_required
def create_task():
    data = request.get_json(silent=True) or {}
    required = ["title", "description", "project_id", "assigned_to", "status", "priority", "due_date"]
    validation = require_fields(data, required)
    if validation:
        return validation

    if data["status"] not in ["Pending", "In Progress", "Completed"]:
        return jsonify({"error": "Invalid status"}), 400
    if data["priority"] not in ["Low", "Medium", "High", "Critical"]:
        return jsonify({"error": "Invalid priority"}), 400

    project = Project.query.get(data["project_id"])
    user = User.query.get(data["assigned_to"])
    if not project or not user:
        return jsonify({"error": "Invalid project_id or assigned_to"}), 400

    task = Task(
        title=data["title"].strip(),
        description=data["description"].strip(),
        project_id=project.id,
        assigned_to=user.id,
        created_by=current_user.id,
        status=data["status"],
        priority=data["priority"],
        due_date=data["due_date"],
    )
    db.session.add(task)

    membership = ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first()
    if not membership:
        db.session.add(ProjectMember(project_id=project.id, user_id=user.id, role="member"))

    db.session.commit()
    return jsonify(serialize_task(task)), 201


@api_bp.get("/tasks/<int:task_id>")
@login_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not current_user.is_admin() and task.assigned_to != current_user.id:
        return jsonify({"error": "You can only view assigned tasks"}), 403
    return jsonify(serialize_task(task))


@api_bp.patch("/tasks/<int:task_id>/status")
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    if not current_user.is_admin() and task.assigned_to != current_user.id:
        return jsonify({"error": "You cannot update this task"}), 403

    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in ["Pending", "In Progress", "Completed"]:
        return jsonify({"error": "Invalid status"}), 400

    task.status = status
    db.session.commit()
    return jsonify(serialize_task(task))
