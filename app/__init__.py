from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    database_url = os.getenv("DATABASE_URL", "sqlite:///taskmanager.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.projects.routes import projects_bp
    from app.tasks.routes import tasks_bp
    from app.api import api_bp
    from app.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        from app.models import User, Project, ProjectMember, Task, Comment
        db.create_all()
        create_demo_data()

    return app


def create_demo_data():
    from app.models import User, Project, ProjectMember, Task
    if User.query.filter_by(email="admin@example.com").first():
        return

    admin = User(
        name="Demo Admin",
        email="admin@example.com",
        password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="admin"
    )
    member = User(
        name="Demo Member",
        email="member@example.com",
        password_hash=bcrypt.generate_password_hash("member123").decode("utf-8"),
        role="member"
    )
    db.session.add_all([admin, member])
    db.session.commit()

    project = Project(
        title="Company Website Redesign",
        description="Redesign the company website with modern UI and task tracking.",
        deadline="2026-06-30",
        created_by=admin.id
    )
    db.session.add(project)
    db.session.commit()

    membership1 = ProjectMember(project_id=project.id, user_id=admin.id, role="admin")
    membership2 = ProjectMember(project_id=project.id, user_id=member.id, role="member")
    task = Task(
        title="Create landing page UI",
        description="Design and implement the homepage using Bootstrap.",
        project_id=project.id,
        assigned_to=member.id,
        created_by=admin.id,
        status="In Progress",
        priority="High",
        due_date="2026-06-10"
    )
    db.session.add_all([membership1, membership2, task])
    db.session.commit()
