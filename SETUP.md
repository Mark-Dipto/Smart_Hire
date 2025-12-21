# Quick Setup Guide

## Step 1: Install Dependencies

In Replit or your terminal, run:
```bash
pip install -r requirements.txt
```

## Step 2: Configure Database

1. Open `config.py`
2. Update the database credentials:
   ```python
   DB_CONFIG = {
       'host': 'sql12.freesqldatabase.com',
       'database': 'sql12812279',
       'user': 'your_actual_username',      # Replace this
       'password': 'your_actual_password'   # Replace this
   }
   ```

## Step 3: Run the Application

In Replit, just click "Run" or in terminal:
```bash
python app.py
```

The app will be available at: `http://localhost:5000` (or the Replit URL)

## Step 4: Test the Application

1. **Register as a Candidate:**
   - Go to Register
   - Fill in your details
   - Select "Job Seeker / Candidate"
   - Register

2. **Upload a Resume:**
   - Login as candidate
   - Go to "Upload Resume"
   - Upload a PDF, DOC, or DOCX file
   - System will extract skills automatically

3. **Register as a Recruiter:**
   - Logout
   - Register as "Recruiter"
   - Login

4. **Post a Job:**
   - Go to "Post New Job"
   - Fill in job details
   - Add required skills (comma-separated)
   - Post the job

5. **View Matches:**
   - As candidate: Go to "Job Matches" to see matching jobs
   - As recruiter: Click "View Matches" on any job to see matching candidates

## Notes

- The resume text extraction is simplified. For better results, you can add PyPDF2 to requirements.txt for PDF parsing
- Make sure your database has all the tables from the SQL dump
- The matching algorithm calculates scores based on skill overlap percentage

## Troubleshooting

**Database Connection Error:**
- Check your database credentials in `config.py`
- Verify your database is accessible from your IP (if using free hosting)

**File Upload Error:**
- Make sure the `uploads/resumes/` directory exists (it's created automatically)
- Check file size (max 5MB)
- Verify file type (PDF, DOC, DOCX only)

**No Matches Showing:**
- Make sure you've uploaded a resume (for candidates)
- Make sure jobs are posted (for recruiters)
- Verify skills are being extracted correctly

