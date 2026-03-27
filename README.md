# Job Application Tracker

A REST API built with Python and Flask to track job applications,
interview stages, and notes — with a clean frontend dashboard.

## Live Demo

- Frontend: https://myjobtracker2.netlify.app/
- Backend API: https://job-tracker-xjbi.onrender.com

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** PostgreSQL (Supabase)
- **Auth:** Flask-Login, bcrypt
- **Frontend:** HTML, CSS, Vanilla JavaScript (fetch API)
- **Deployment:** Render (backend), Netlify (frontend)

## Features

- User registration and login
- Add job applications with company, role and status
- Update application status (applied/interview/offer/rejected)
- Delete applications
- Dashboard with live stats

## API Endpoints

### Auth

| Method | Endpoint       | Description    |
| ------ | -------------- | -------------- |
| POST   | /auth/register | Create account |
| POST   | /auth/login    | Login          |
| POST   | /auth/logout   | Logout         |

### Jobs

| Method | Endpoint    | Description         |
| ------ | ----------- | ------------------- |
| GET    | /jobs/      | Get all jobs        |
| POST   | /jobs/      | Add new job         |
| PUT    | /jobs/<id>  | Update job          |
| DELETE | /jobs/<id>  | Delete job          |
| GET    | /jobs/stats | Get dashboard stats |

## Run Locally

1. Clone the repo
   git clone https://github.com/yourname/job-tracker.git

2. Create virtual environment
   python -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file
   DATABASE_URL=postgresql://yourname@localhost:5432/job_tracker
   SECRET_KEY=your-secret-key

5. Run migrations
   flask db upgrade

6. Start the app
   python run.py
