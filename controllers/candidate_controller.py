"""Candidate controller"""
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from controllers.auth_controller import is_logged_in, is_candidate
from models.resume_model import ResumeModel
from models.job_model import JobModel
from models.skill_model import SkillModel
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def candidate_dashboard():
    """Candidate dashboard"""
    if not is_logged_in() or not is_candidate():
        flash('Please login as a candidate', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    resumes = ResumeModel.get_resumes_by_candidate(user_id)
    
    # Get candidate profile (if exists)
    from models.database import get_db_connection
    conn = get_db_connection()
    profile = None
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
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

def candidate_matches():
    """Show job matches for candidate"""
    if not is_logged_in() or not is_candidate():
        flash('Please login as a candidate', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
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

