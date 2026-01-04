"""Main controller for home page and public routes"""
from flask import render_template, redirect, url_for, session, request, flash, send_from_directory, current_app
from controllers.auth_controller import is_logged_in, is_candidate
from models.job_model import JobModel
from models.skill_model import SkillModel
from models.resume_model import ResumeModel

def index():
    """Landing page route"""
    return render_template('index.html')

def recruiter_landing():
    """Landing page specifically for recruiters"""
    return render_template('recruiter_landing.html')

def careers():
    """Careers page with job search, sorting, and skill matching"""
    if is_logged_in() and session.get('role') == 'recruiter':
        flash('Recruiters cannot browse jobs. Please manage your postings from the dashboard.', 'warning')
        return redirect(url_for('recruiter_dashboard'))

    query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'date')
    
    if query:
        jobs = JobModel.search_jobs(query)
    else:
        jobs = JobModel.get_active_jobs()
        
    processed_jobs = []
    
    candidate_skill_ids = set()
    is_candidate_logged_in = is_logged_in() and is_candidate()
    resume_text = ""
    
    if is_candidate_logged_in:
        candidate_skills = SkillModel.get_candidate_skills(session['user_id'])
        candidate_skill_ids = set(candidate_skills.keys())
        resume_text = ResumeModel.get_latest_resume_text(session['user_id'])

    for job in jobs:
        job_data = dict(job)
        job_data['match_score'] = 0
        job_data['matching_skills'] = []
        job_data['missing_skills'] = []
        
        if is_candidate_logged_in:
            job_skills = SkillModel.get_job_skills(job['job_id'])
            job_skill_ids = set(job_skills.keys())
            
            # Calculate Advanced Score
            job_data['match_score'] = SkillModel.calculate_match_score(
                candidate_skill_ids, 
                job_skill_ids,
                resume_text=resume_text,
                job_description=job['description'],
                job_title=job['title']
            )
            
            matching_ids = candidate_skill_ids.intersection(job_skill_ids)
            missing_ids = job_skill_ids - candidate_skill_ids
            
            job_data['matching_skills'] = [candidate_skills[sid] for sid in matching_ids]
            job_data['missing_skills'] = [job_skills[sid] for sid in missing_ids]
            
        processed_jobs.append(job_data)
    
    if sort_by == 'match' and is_candidate_logged_in:
        processed_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    return render_template('careers.html', jobs=processed_jobs, query=query, sort_by=sort_by)

def download_resume(filename):
    """Serve uploaded resume"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)