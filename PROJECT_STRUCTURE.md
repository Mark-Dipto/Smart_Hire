# Project Structure

```
PROJECT/
│
├── app.py                    # App starter only - initializes Flask and registers routes
├── config.py                 # Configuration (database, app settings)
│
├── controllers/              # Controllers (Business Logic)
│   ├── __init__.py
│   ├── main_controller.py    # Home/index routes
│   ├── auth_controller.py    # Login, register, logout
│   ├── candidate_controller.py  # Candidate routes
│   └── recruiter_controller.py  # Recruiter routes
│
├── models/                   # Models (Database Operations)
│   ├── __init__.py
│   ├── database.py            # Database connection
│   ├── user_model.py         # User operations
│   ├── resume_model.py       # Resume operations
│   ├── job_model.py          # Job operations
│   └── skill_model.py        # Skill operations
│
├── templates/                # Views (HTML Templates)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── candidate_dashboard.html
│   ├── upload_resume.html
│   ├── candidate_matches.html
│   ├── recruiter_dashboard.html
│   ├── create_job.html
│   └── job_matches.html
│
├── static/                   # Static Files (CSS, JS, Images)
│   └── style.css
│
├── uploads/                  # Uploaded Files (created automatically)
│   └── resumes/
│
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── SETUP.md                  # Setup instructions
```

## MVC Architecture

### Model (models/)
- **database.py**: Handles database connections
- **user_model.py**: User registration, login, user data
- **resume_model.py**: Resume upload, text extraction, skill extraction
- **job_model.py**: Job creation, retrieval
- **skill_model.py**: Skill management, matching algorithm

### View (templates/)
- HTML templates for all pages
- Uses Jinja2 templating
- Links to static CSS file

### Controller (controllers/)
- **main_controller.py**: Home page logic
- **auth_controller.py**: Authentication logic
- **candidate_controller.py**: Candidate-specific routes
- **recruiter_controller.py**: Recruiter-specific routes

### Static Files (static/)
- **style.css**: All CSS styles (moved from inline styles)

## Flow

1. **app.py** initializes Flask app and registers all routes
2. **Routes** point to controller functions
3. **Controllers** call model methods for database operations
4. **Models** interact with database and return data
5. **Controllers** render templates with data
6. **Templates** display HTML with CSS from static folder

## Benefits of This Structure

✅ **Separation of Concerns**: Each layer has a specific responsibility
✅ **Maintainability**: Easy to find and modify code
✅ **Scalability**: Easy to add new features
✅ **Testability**: Each component can be tested independently
✅ **Beginner-Friendly**: Clear structure, easy to understand

