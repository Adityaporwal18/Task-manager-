from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.forms import ProjectForm
from app.models import Project, ProjectMember, User, Task

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard.dashboard"))
        return func(*args, **kwargs)
    return wrapper


@projects_bp.route("/")
@login_required
def list_projects():
    if current_user.is_admin():
        projects = Project.query.order_by(Project.created_at.desc()).all()
    else:
        memberships = ProjectMember.query.filter_by(user_id=current_user.id).all()
        project_ids = [m.project_id for m in memberships]
        projects = Project.query.filter(Project.id.in_(project_ids)).all() if project_ids else []
    return render_template("projects/projects.html", projects=projects)


@projects_bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            deadline=str(form.deadline.data),
            created_by=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        db.session.add(ProjectMember(project_id=project.id, user_id=current_user.id, role="admin"))
        db.session.commit()
        flash("Project created successfully.", "success")
        return redirect(url_for("projects.detail_project", project_id=project.id))
    return render_template("projects/create_project.html", form=form, title="Create Project")


@projects_bp.route("/<int:project_id>")
@login_required
def detail_project(project_id):
    project = Project.query.get_or_404(project_id)
    if not current_user.is_admin():
        membership = ProjectMember.query.filter_by(project_id=project.id, user_id=current_user.id).first()
        if not membership:
            flash("You are not a member of this project.", "danger")
            return redirect(url_for("dashboard.dashboard"))
    members = ProjectMember.query.filter_by(project_id=project.id).all()
    users = User.query.all()
    tasks = Task.query.filter_by(project_id=project.id).all()
    return render_template("projects/project_detail.html", project=project, members=members, users=users, tasks=tasks)


@projects_bp.route("/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data.strip()
        project.description = form.description.data.strip()
        project.deadline = str(form.deadline.data)
        db.session.commit()
        flash("Project updated successfully.", "success")
        return redirect(url_for("projects.detail_project", project_id=project.id))
    form.title.data = project.title
    form.description.data = project.description
    return render_template("projects/create_project.html", form=form, title="Edit Project")


@projects_bp.route("/<int:project_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully.", "info")
    return redirect(url_for("projects.list_projects"))


@projects_bp.route("/<int:project_id>/add-member", methods=["POST"])
@login_required
@admin_required
def add_member(project_id):
    project = Project.query.get_or_404(project_id)
    user_id = request.form.get("user_id")
    if not user_id:
        flash("Please select a user.", "warning")
        return redirect(url_for("projects.detail_project", project_id=project.id))
    existing = ProjectMember.query.filter_by(project_id=project.id, user_id=int(user_id)).first()
    if existing:
        flash("User is already in this project.", "warning")
    else:
        db.session.add(ProjectMember(project_id=project.id, user_id=int(user_id), role="member"))
        db.session.commit()
        flash("Member added successfully.", "success")
    return redirect(url_for("projects.detail_project", project_id=project.id))
