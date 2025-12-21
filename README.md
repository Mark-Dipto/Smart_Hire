# SmartHire - Intelligent Resume Matching Platform

SmartHire is an MVC-based web platform that analyzes resumes, matches them with job descriptions, and gives users personalized career insights (skill gaps, recommended roles, learning paths).

## Features

### Functional Requirements
- **FR1** - User Registration and Login: Users (job seekers and recruiters) can register and log in using email and password
- **FR2** - Resume Upload: Job seekers can upload resume files (PDF, DOC, DOCX)
- **FR3** - Resume Analysis: System extracts key information (skills, education, work experience) from resumes
- **FR4** - Job Posting Management: Recruiters can create, edit, and delete job postings with required skills
- **FR5** - Resume-Job Matching: System calculates match scores and displays ranked lists of matching jobs/candidates

### Non-Functional Requirements
- **NFR1** - Performance: Matching results displayed within 5 seconds
- **NFR2** - Usability: Intuitive UI for easy navigation
- **NFR3** - Security: Passwords stored in hashed form, access restrictions
- **NFR4** - Reliability: Graceful error handling
- **NFR5** - Compatibility: Works on Chrome, Firefox, and Edge

## Project Structure

```
Project/
├── app.py                 # App starter - initializes Flask and registers routes
├── config.py              # Database and app configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── controllers/           # Controllers (Business Logic)
│   ├── main_controller.py
│   ├── auth_controller.py
│   ├── candidate_controller.py
│   └── recruiter_controller.py
├── models/                # Models (Database Operations)
│   ├── database.py
│   ├── user_model.py
│   ├── resume_model.py
│   ├── job_model.py
│   └── skill_model.py
├── templates/             # Views (HTML Templates)
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
├── static/                # Static Files (CSS)
│   └── style.css
└── uploads/               # Uploaded resume files
    └── resumes/
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Edit `config.py` and update the database credentials:

```python
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'database': 'sql12812279',
    'user': 'your_username',      # Update this
    'password': 'your_password'   # Update this
}
```

### 3. Run the Application

```bash
python app.py
```

The application will run on `http://localhost:5000`

## Usage

### For Candidates (Job Seekers)
1. Register/Login as a candidate
2. Upload your resume (PDF, DOC, or DOCX)
3. System automatically extracts your skills
4. View job matches ranked by compatibility
5. See skill gaps and matching skills for each job

### For Recruiters
1. Register/Login as a recruiter
2. Post job openings with required skills
3. View matched candidates ranked by compatibility
4. See which candidates have matching skills and what they're missing

## Technology Stack

- **Backend**: Flask (Python) - MVC Architecture
- **Database**: MySQL (phpMyAdmin)
- **Frontend**: HTML, CSS (static files)
- **File Upload**: Werkzeug

## Database Schema

The application uses the following main tables:
- `users` - User accounts
- `candidates` - Candidate-specific data
- `recruiters` - Recruiter-specific data
- `resumes` - Uploaded resume files
- `jobs` - Job postings
- `skills` - Available skills
- `candidate_skills` - Skills associated with candidates
- `job_skills` - Skills required for jobs
- `match_results` - Stored match calculations

## Security Features

- Passwords are hashed using SHA-256 (for production, consider bcrypt)
- Session-based authentication
- File upload validation (type and size)
- SQL injection prevention using parameterized queries
- Access control based on user roles

## Notes

- The resume text extraction is simplified. For production, consider using libraries like PyPDF2 for PDF parsing
- The matching algorithm is based on skill overlap percentage
- All templates use inline CSS for simplicity and beginner-friendliness
- The application follows MVC pattern with clear separation of concerns

## Future Enhancements

- Advanced resume parsing (education, experience extraction)
- Machine learning-based matching
- Email notifications
- Advanced search and filtering
- Career insights dashboard
- Learning path recommendations

## License

This project is created for educational purposes.

