# Team Task Manager - Full Stack Flask App

A full-stack Team Task Manager web app where users can create projects, assign tasks, track progress, and work with role-based access for Admin and Member users.

## Live Submission

- Live URL: https://web-production-bf014f.up.railway.app
- GitHub Repo: https://github.com/Adityaporwal18/Task-manager-

## Features

- User signup, login, and logout
- Password hashing with Flask-Bcrypt
- Admin and Member roles
- Role-based access control
- Admin dashboard with projects, users, tasks, and overdue task counts
- Member dashboard with assigned projects, assigned tasks, and overdue work
- Project creation, editing, deletion, and member management
- Task creation, assignment, editing, deletion, and status updates
- Task priority, due date, overdue detection, and comments
- Search and status filtering for tasks
- REST API endpoints for projects, tasks, status updates, and dashboard summaries
- SQLite database with SQLAlchemy models and relationships
- Responsive Bootstrap UI
- Railway deployment with Gunicorn

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-WTF
- SQLite
- Bootstrap 5
- Gunicorn
- Railway

## Database Models

- `User`: stores users, hashed passwords, and roles
- `Project`: stores project details and deadlines
- `ProjectMember`: links users to projects
- `Task`: stores assignments, status, priority, and due dates
- `Comment`: stores task comments

## REST API Endpoints

Most API routes require login. Admin-only routes require an Admin user.

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/health` | Health check |
| GET | `/api/dashboard` | Dashboard summary for current user |
| GET | `/api/projects` | List visible projects |
| POST | `/api/projects` | Create project, Admin only |
| GET | `/api/projects/<id>` | Get one project |
| GET | `/api/tasks` | List visible tasks |
| POST | `/api/tasks` | Create task, Admin only |
| GET | `/api/tasks/<id>` | Get one task |
| PATCH | `/api/tasks/<id>/status` | Update task status |

Example task status update:

```bash
curl -X PATCH https://web-production-bf014f.up.railway.app/api/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"Completed"}'
```

## Demo Login

Demo users are created automatically when the app starts for the first time.

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

## Local Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

Mac/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Packages

```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
python run.py
```

Open:

```txt
http://127.0.0.1:5000
```

## Railway Deployment

This app is deployed on Railway.

Required environment variable:

```txt
SECRET_KEY=your-production-secret-key
```

Production start command:

```bash
gunicorn run:app --bind 0.0.0.0:$PORT
```

## Assignment Checklist

- Authentication: Done
- Project and team management: Done
- Task creation, assignment, and status tracking: Done
- Dashboard with tasks, status, and overdue work: Done
- REST APIs: Done
- Database with relationships: Done
- Validations: Done
- Role-based access control: Done
- Railway deployment: Done
- GitHub repository and README: Done

## Note

SQLite is used for simple deployment and local development. For larger production usage, the app can be moved to PostgreSQL by setting `DATABASE_URL`.
