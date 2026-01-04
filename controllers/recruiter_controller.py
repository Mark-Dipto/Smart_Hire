"""Recruiter controller"""
from flask import render_template, request, redirect, url_for, session, flash
from controllers.auth_controller import is_logged_in, is_recruiter
from models.job_model import JobModel
from models.skill_model import SkillModel
<<<<<<< HEAD

def recruiter_dashboard():
    """Recruiter dashboard"""
=======
from models.application_model import ApplicationModel
import os

def recruiter_dashboard():
    """Recruiter dashboard with stats"""
>>>>>>> 60a626c (Resolve merge conflicts)
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    jobs = JobModel.get_jobs_by_recruiter(user_id)
    
<<<<<<< HEAD
    return render_template('recruiter_dashboard.html', jobs=jobs)
=======
    # Calculate Stats
    active_jobs_count = sum(1 for job in jobs if job['is_active'])
    
    # Get total applications across all jobs
    total_apps = 0
    for job in jobs:
        apps = ApplicationModel.get_applications_by_job(job['job_id'])
        total_apps += len(apps)
    
    stats = {
        'active_jobs': active_jobs_count,
        'total_jobs': len(jobs),
        'total_applications': total_apps
    }
    
    return render_template('recruiter_dashboard.html', jobs=jobs, stats=stats)
>>>>>>> 60a626c (Resolve merge conflicts)

def create_job():
    """Handle job creation"""
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        skills_input = request.form.get('skills', '')
        
        if not all([title, description]):
            flash('Title and description are required', 'error')
            return render_template('create_job.html')
        
        # Create job
        result = JobModel.create_job(session['user_id'], title, description, location)
        
        if result['success']:
            job_id = result['job_id']
            
            # Process skills
            skills_list = [s.strip().lower() for s in skills_input.split(',') if s.strip()]
            for skill_name in skills_list:
                skill_id = SkillModel.get_or_create_skill(skill_name)
                if skill_id:
                    SkillModel.link_skill_to_job(job_id, skill_id)
            
            flash('Job posted successfully!', 'success')
            return redirect(url_for('recruiter_dashboard'))
        else:
            flash(result['message'], 'error')
    
    return render_template('create_job.html')

def job_matches(job_id):
<<<<<<< HEAD
    """Show candidate matches for a job"""
=======
    """Show candidate matches for a job (AI Matches)"""
>>>>>>> 60a626c (Resolve merge conflicts)
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))
    
    # Verify job belongs to recruiter
    job = JobModel.get_job_by_id(job_id, session['user_id'])
    
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('recruiter_dashboard'))
    
    # Get job skills
    job_skills = SkillModel.get_job_skills(job_id)
    job_skill_ids = set(job_skills.keys())
    
    # Get all candidates with resumes
    candidates = SkillModel.get_all_candidates_with_resumes()
    
    # Calculate match scores
    matches = []
    for candidate in candidates:
        # Get candidate skills
        candidate_skills = SkillModel.get_candidate_skills(candidate['candidate_id'])
        candidate_skill_ids = set(candidate_skills.keys())
        
        # Calculate match score
        match_score = SkillModel.calculate_match_score(candidate_skill_ids, job_skill_ids)
        matching_skills = candidate_skill_ids.intersection(job_skill_ids)
        
        matches.append({
            'candidate': candidate,
            'match_score': match_score,
            'matching_skills': [candidate_skills[sid] for sid in matching_skills if sid in candidate_skills],
            'missing_skills': [job_skills[sid] for sid in job_skill_ids - candidate_skill_ids]
        })
    
    # Sort by match score
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    return render_template('job_matches.html', job=job, matches=matches)

<<<<<<< HEAD
=======
def job_applications(job_id):
    """Show actual applications for a job"""
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))
    
    # Verify job belongs to recruiter
    job = JobModel.get_job_by_id(job_id, session['user_id'])
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('recruiter_dashboard'))
    
    # Get applications
    applications = ApplicationModel.get_applications_by_job(job_id)
    
    # Calculate match scores for applicants and extract filename
    job_skills = SkillModel.get_job_skills(job_id)
    job_skill_ids = set(job_skills.keys())
    
    for app in applications:
        # Calculate score
        candidate_skills = SkillModel.get_candidate_skills(app['candidate_id'])
        candidate_skill_ids = set(candidate_skills.keys())
        app['match_score'] = SkillModel.calculate_match_score(candidate_skill_ids, job_skill_ids)
        
        # Extract filename for resume link
        if app.get('resume_path'):
            app['resume_filename'] = os.path.basename(app['resume_path'])
    
    return render_template('job_applications.html', job=job, applications=applications)

def update_application_status(application_id):
    """Handle application Accept/Reject"""
    if not is_logged_in() or not is_recruiter():
        flash('Access denied', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        status = request.form.get('status')
        job_id = request.form.get('job_id')
        
        if status in ['accepted', 'rejected']:
            ApplicationModel.update_status(application_id, status)
            flash(f'Application {status} successfully', 'success')
        
        return redirect(url_for('job_applications', job_id=job_id))
    
    return redirect(url_for('recruiter_dashboard'))
>>>>>>> 60a626c (Resolve merge conflicts)
