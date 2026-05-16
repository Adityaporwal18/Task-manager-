# Team Task Manager - Flask Full Stack App

A professional full-stack Team Task Manager web app using Flask, SQLite, SQLAlchemy, Flask-Login, and Bootstrap.

## Features

- User signup/login/logout
- Admin and Member roles
- Admin dashboard
- Member dashboard
- Project creation and management
- Add team members to projects
- Task creation and assignment
- Task status tracking
- Priority and due date support
- Overdue task highlighting
- Task comments
- Search/filter tasks
- Responsive Bootstrap UI
- SQLite database for local development
- Ready for Railway deployment

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- SQLite
- Bootstrap 5
- Gunicorn

## Local Setup

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python run.py
```

Open:

```txt
http://127.0.0.1:5000
```

## Demo Login

When you first run the app, demo users are automatically created.

### Admin

```txt
Email: admin@example.com
Password: admin123
```

### Member

```txt
Email: member@example.com
Password: member123
```

## Railway Deployment

1. Push code to GitHub
2. Create new Railway project
3. Connect GitHub repository
4. Add environment variables:

```txt
SECRET_KEY=your-production-secret-key
```

5. Deploy

## Important Note

This project uses SQLite for easiest setup. For large production usage, switch to PostgreSQL later by changing `DATABASE_URL`.
