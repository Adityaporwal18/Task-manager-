from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import TaskForm, CommentForm
from app.models import Task, Project, User, ProjectMember, Comment

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard.dashboard"))
        return func(*args, **kwargs)
    return wrapper


def set_task_choices(form):
    form.project_id.choices = [(p.id, p.title) for p in Project.query.order_by(Project.title).all()]
    form.assigned_to.choices = [(u.id, f"{u.name} ({u.role})") for u in User.query.order_by(User.name).all()]


@tasks_bp.route("/")
@login_required
def list_tasks():
    status = request.args.get("status", "")
    search = request.args.get("search", "")
    query = Task.query
    if not current_user.is_admin():
        query = query.filter_by(assigned_to=current_user.id)
    if status:
        query = query.filter_by(status=status)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    tasks = query.order_by(Task.created_at.desc()).all()
    return render_template("tasks/tasks.html", tasks=tasks, status=status, search=search)


@tasks_bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_task():
    form = TaskForm()
    set_task_choices(form)
    if not form.project_id.choices:
        flash("Create a project first.", "warning")
        return redirect(url_for("projects.create_project"))
    if form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            project_id=form.project_id.data,
            assigned_to=form.assigned_to.data,
            created_by=current_user.id,
            status=form.status.data,
            priority=form.priority.data,
            due_date=str(form.due_date.data)
        )
        db.session.add(task)
        exists = ProjectMember.query.filter_by(project_id=form.project_id.data, user_id=form.assigned_to.data).first()
        if not exists:
            db.session.add(ProjectMember(project_id=form.project_id.data, user_id=form.assigned_to.data, role="member"))
        db.session.commit()
        flash("Task created successfully.", "success")
        return redirect(url_for("tasks.detail_task", task_id=task.id))
    return render_template("tasks/create_task.html", form=form, title="Create Task")


@tasks_bp.route("/<int:task_id>", methods=["GET", "POST"])
@login_required
def detail_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not current_user.is_admin() and task.assigned_to != current_user.id:
        flash("You can only view assigned tasks.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(task_id=task.id, user_id=current_user.id, message=form.message.data.strip())
        db.session.add(comment)
        db.session.commit()
        flash("Comment added.", "success")
        return redirect(url_for("tasks.detail_task", task_id=task.id))
    return render_template("tasks/task_detail.html", task=task, form=form)


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()
    set_task_choices(form)
    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = form.description.data.strip()
        task.project_id = form.project_id.data
        task.assigned_to = form.assigned_to.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = str(form.due_date.data)
        db.session.commit()
        flash("Task updated successfully.", "success")
        return redirect(url_for("tasks.detail_task", task_id=task.id))
    form.title.data = task.title
    form.description.data = task.description
    form.project_id.data = task.project_id
    form.assigned_to.data = task.assigned_to
    form.status.data = task.status
    form.priority.data = task.priority
    return render_template("tasks/create_task.html", form=form, title="Edit Task")


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully.", "info")
    return redirect(url_for("tasks.list_tasks"))


@tasks_bp.route("/<int:task_id>/status", methods=["POST"])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    if not current_user.is_admin() and task.assigned_to != current_user.id:
        flash("You cannot update this task.", "danger")
        return redirect(url_for("tasks.list_tasks"))
    new_status = request.form.get("status")
    if new_status in ["Pending", "In Progress", "Completed"]:
        task.status = new_status
        db.session.commit()
        flash("Task status updated.", "success")
    return redirect(url_for("tasks.detail_task", task_id=task.id))
