from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    role = SelectField("Role", choices=[("member", "Member"), ("admin", "Admin")], validators=[DataRequired()])
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProjectForm(FlaskForm):
    title = StringField("Project Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[DataRequired()])
    deadline = DateField("Deadline", validators=[DataRequired()])
    submit = SubmitField("Save Project")


class TaskForm(FlaskForm):
    title = StringField("Task Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[DataRequired()])
    project_id = SelectField("Project", coerce=int, validators=[DataRequired()])
    assigned_to = SelectField("Assign To", coerce=int, validators=[DataRequired()])
    status = SelectField("Status", choices=[("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed")])
    priority = SelectField("Priority", choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Critical", "Critical")])
    due_date = DateField("Due Date", validators=[DataRequired()])
    submit = SubmitField("Save Task")


class CommentForm(FlaskForm):
    message = TextAreaField("Comment", validators=[DataRequired(), Length(min=2)])
    submit = SubmitField("Add Comment")
