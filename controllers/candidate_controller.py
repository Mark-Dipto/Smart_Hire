"""Candidate controller"""
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from controllers.auth_controller import is_logged_in, is_candidate
from models.resume_model import ResumeModel
from models.job_model import JobModel
from models.skill_model import SkillModel
<<<<<<< HEAD
=======
from models.application_model import ApplicationModel  # Import ApplicationModel
>>>>>>> 60a626c (Resolve merge conflicts)
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def candidate_dashboard():
<<<<<<< HEAD
    """Candidate dashboard"""
=======
    """Candidate dashboard with stats, applications, and top matches"""
>>>>>>> 60a626c (Resolve merge conflicts)
    if not is_logged_in() or not is_candidate():
        flash('Please login as a candidate', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
<<<<<<< HEAD
    resumes = ResumeModel.get_resumes_by_candidate(user_id)
    
    # Get candidate profile (if exists)
=======
    
    # 1. Get Resumes
    resumes = ResumeModel.get_resumes_by_candidate(user_id)
    
    # 2. Get Profile
>>>>>>> 60a626c (Resolve merge conflicts)
    from models.database import get_db_connection
    conn = get_db_connection()
    profile = None
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
<<<<<<< HEAD
            cursor.execute(
                "SELECT * FROM candidate_profiles WHERE candidate_id = %s",
                (user_id,)
            )
            profile = cursor.fetchone()
            conn.close()
        except:
            if conn:
                conn.close()
    
    return render_template('candidate_dashboard.html', resumes=resumes, profile=profile)
=======
            cursor.execute("SELECT * FROM candidate_profiles WHERE candidate_id = %s", (user_id,))
            profile = cursor.fetchone()
            conn.close()
        except:
            if conn: conn.close()

    # 3. Get Applications (NEW)
    applications = ApplicationModel.get_applications_by_candidate(user_id)

    # 4. Calculate Matches & Stats
    active_jobs = JobModel.get_active_jobs()
    candidate_skills = SkillModel.get_candidate_skills(user_id)
    candidate_skill_ids = set(candidate_skills.keys())
    
    matches = []
    high_matches_count = 0
    
    # Get IDs of jobs already applied to
    applied_job_ids = [app['job_id'] for app in applications]

    for job in active_jobs:
        # Skip jobs user has already applied to in the "Top Matches" suggestion list
        if job['job_id'] in applied_job_ids:
            continue

        job_skills = SkillModel.get_job_skills(job['job_id'])
        job_skill_ids = set(job_skills.keys())
        match_score = SkillModel.calculate_match_score(candidate_skill_ids, job_skill_ids)
        
        if match_score > 0:
            matches.append({
                'job': job,
                'match_score': match_score
            })
            if match_score > 60:
                high_matches_count += 1
                
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    top_matches = matches[:3]

    stats = {
        'resumes': len(resumes),
        'high_matches': high_matches_count,
        'applications': len(applications)
    }
    
    return render_template('candidate_dashboard.html', 
                         resumes=resumes, 
                         profile=profile, 
                         stats=stats, 
                         top_matches=top_matches,
                         applications=applications) # Pass applications to template
>>>>>>> 60a626c (Resolve merge conflicts)

def upload_resume():
    """Handle resume upload"""
    if not is_logged_in() or not is_candidate():
        flash('Please login as a candidate', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Extract text from resume
            parsed_text = ResumeModel.extract_text_from_resume(file_path)
            
            # Save to database
            result = ResumeModel.save_resume(session['user_id'], file_path, parsed_text)
            
            if result['success']:
                # Extract and save skills
                skills = ResumeModel.extract_skills(parsed_text)
                for skill_name in skills:
                    skill_id = SkillModel.get_or_create_skill(skill_name)
                    if skill_id:
                        SkillModel.link_skill_to_candidate(session['user_id'], skill_id)
                
                flash('Resume uploaded and analyzed successfully!', 'success')
                return redirect(url_for('candidate_dashboard'))
            else:
                flash(result['message'], 'error')
    
    return render_template('upload_resume.html')

<<<<<<< HEAD
def candidate_matches():
    """Show job matches for candidate"""
    if not is_logged_in() or not is_candidate():
        flash('Please login as a candidate', 'error')
=======
def apply_job(job_id):
    """Handle job application"""
    if not is_logged_in() or not is_candidate():
        flash('You must be logged in as a candidate to apply.', 'error')
>>>>>>> 60a626c (Resolve merge conflicts)
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
<<<<<<< HEAD
    # Get candidate's skills
    candidate_skills = SkillModel.get_candidate_skills(user_id)
    candidate_skill_ids = set(candidate_skills.keys())
    
    # Get all active jobs
    jobs = JobModel.get_active_jobs()
    
    # Calculate match scores
    matches = []
    for job in jobs:
        # Get job skills
        job_skills = SkillModel.get_job_skills(job['job_id'])
        job_skill_ids = set(job_skills.keys())
        
        # Calculate match score
        match_score = SkillModel.calculate_match_score(candidate_skill_ids, job_skill_ids)
        matching_skills = candidate_skill_ids.intersection(job_skill_ids)
        
        matches.append({
            'job': job,
            'match_score': match_score,
            'matching_skills': [candidate_skills[sid] for sid in matching_skills],
            'missing_skills': [job_skills[sid] for sid in job_skill_ids - candidate_skill_ids]
        })
    
    # Sort by match score
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    return render_template('candidate_matches.html', matches=matches)

=======
    # Check if already applied
    if ApplicationModel.has_applied(user_id, job_id):
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('careers'))
        
    result = ApplicationModel.create_application(job_id, user_id)
    
    if result['success']:
        flash('Application sent successfully! Good luck.', 'success')
    else:
        flash(result.get('message', 'An error occurred'), 'error')
        
    return redirect(url_for('careers'))
>>>>>>> 60a626c (Resolve merge conflicts)
