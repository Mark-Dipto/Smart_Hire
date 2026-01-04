"""Candidate controller"""
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from controllers.auth_controller import is_logged_in, is_candidate
from models.resume_model import ResumeModel
from models.job_model import JobModel
from models.skill_model import SkillModel
from models.application_model import ApplicationModel
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def candidate_dashboard():
    """Candidate dashboard with stats, applications, and top matches"""
    if not is_logged_in() or not is_candidate():
        flash('Please login as a candidate', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    resumes = ResumeModel.get_resumes_by_candidate(user_id)
    
    # Get Resume Text for AI Analysis
    resume_text = ""
    if resumes:
        resume_text = resumes[0]['parsed_text']

    from models.database import get_db_connection
    conn = get_db_connection()
    profile = None
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM candidate_profiles WHERE candidate_id = %s", (user_id,))
            profile = cursor.fetchone()
            conn.close()
        except:
            if conn: conn.close()

    applications = ApplicationModel.get_applications_by_candidate(user_id)
    active_jobs = JobModel.get_active_jobs()
    candidate_skills = SkillModel.get_candidate_skills(user_id)
    candidate_skill_ids = set(candidate_skills.keys())
    
    matches = []
    high_matches_count = 0
    applied_job_ids = [app['job_id'] for app in applications]

    for job in active_jobs:
        if job['job_id'] in applied_job_ids:
            continue

        job_skills = SkillModel.get_job_skills(job['job_id'])
        job_skill_ids = set(job_skills.keys())
        
        # Calculate Advanced Score
        match_score = SkillModel.calculate_match_score(
            candidate_skill_ids, 
            job_skill_ids,
            resume_text=resume_text,
            job_description=job['description'],
            job_title=job['title']
        )
        
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
                         applications=applications)

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
            
            # Use NEW extraction logic
            parsed_text = ResumeModel.extract_text_from_resume(file_path)
            
            result = ResumeModel.save_resume(session['user_id'], file_path, parsed_text)
            
            if result['success']:
                # Use NEW skill extraction
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

def apply_job(job_id):
    """Handle job application"""
    if not is_logged_in() or not is_candidate():
        flash('You must be logged in as a candidate to apply.', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    if ApplicationModel.has_applied(user_id, job_id):
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('careers'))
        
    result = ApplicationModel.create_application(job_id, user_id)
    if result['success']:
        flash('Application sent successfully! Good luck.', 'success')
    else:
        flash(result.get('message', 'An error occurred'), 'error')
        
    return redirect(url_for('careers'))

def respond_to_offer(application_id, status):
    """Handle offer acceptance/rejection"""
    if not is_logged_in() or not is_candidate():
        flash('Access denied', 'error')
        return redirect(url_for('login'))
        
    result = ApplicationModel.respond_to_offer(application_id, status)
    
    if result['success']:
        flash(f'Offer {status} successfully!', 'success')
    else:
        flash(result['message'], 'error')
        
    return redirect(url_for('candidate_dashboard'))