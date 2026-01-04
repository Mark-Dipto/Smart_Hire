"""Recruiter controller"""
from flask import render_template, request, redirect, url_for, session, flash
from controllers.auth_controller import is_logged_in, is_recruiter
from models.job_model import JobModel
from models.skill_model import SkillModel
from models.application_model import ApplicationModel
from models.resume_model import ResumeModel
import os

# ... (Previous imports and functions recruiter_dashboard, create_job remain same)

def recruiter_dashboard():
    """Recruiter dashboard with stats"""
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    jobs = JobModel.get_jobs_by_recruiter(user_id)
    
    active_jobs_count = sum(1 for job in jobs if job['is_active'])
    
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
    """Show candidate matches for a job (AI Matches)"""
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))
    
    # Verify job belongs to recruiter
    job = JobModel.get_job_by_id(job_id, session['user_id'])
    
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('recruiter_dashboard'))
    
    existing_applications = ApplicationModel.get_applications_by_job(job_id)
    app_status_map = {app['candidate_id']: app['status'] for app in existing_applications}

    job_skills = SkillModel.get_job_skills(job_id)
    job_skill_ids = set(job_skills.keys())
    
    candidates = SkillModel.get_all_candidates_with_resumes()
    
    matches = []
    for candidate in candidates:
        candidate_skills = SkillModel.get_candidate_skills(candidate['candidate_id'])
        candidate_skill_ids = set(candidate_skills.keys())
        
        # Get Resume Text for AI Analysis
        resume_text = ResumeModel.get_latest_resume_text(candidate['candidate_id'])
        
        # Calculate Advanced Score
        match_score = SkillModel.calculate_match_score(
            candidate_skill_ids, 
            job_skill_ids, 
            resume_text=resume_text, 
            job_description=job['description'],
            job_title=job['title']
        )
        
        matching_skills = candidate_skill_ids.intersection(job_skill_ids)
        current_status = app_status_map.get(candidate['candidate_id'])

        resumes = ResumeModel.get_resumes_by_candidate(candidate['candidate_id'])
        resume_filename = None
        if resumes:
            resume_path = resumes[0]['file_path']
            resume_filename = os.path.basename(resume_path)

        matches.append({
            'candidate': candidate,
            'match_score': match_score,
            'matching_skills': [candidate_skills[sid] for sid in matching_skills if sid in candidate_skills],
            'missing_skills': [job_skills[sid] for sid in job_skill_ids - candidate_skill_ids],
            'status': current_status,
            'resume_filename': resume_filename
        })
    
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    return render_template('job_matches.html', job=job, matches=matches)

def offer_job(job_id, candidate_id):
    """Offer job to a candidate"""
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))

    result = ApplicationModel.offer_job(job_id, candidate_id)
    
    if result['success']:
        flash('Job offered successfully!', 'success')
    else:
        flash(f"Error offering job: {result.get('message')}", 'error')
        
    return redirect(url_for('job_matches', job_id=job_id))

def job_applications(job_id):
    """Show actual applications for a job"""
    if not is_logged_in() or not is_recruiter():
        flash('Please login as a recruiter', 'error')
        return redirect(url_for('login'))
    
    job = JobModel.get_job_by_id(job_id, session['user_id'])
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('recruiter_dashboard'))
    
    applications = ApplicationModel.get_applications_by_job(job_id)
    job_skills = SkillModel.get_job_skills(job_id)
    job_skill_ids = set(job_skills.keys())
    
    for app in applications:
        candidate_skills = SkillModel.get_candidate_skills(app['candidate_id'])
        candidate_skill_ids = set(candidate_skills.keys())
        
        # Get Resume Text for AI Analysis
        resume_text = ResumeModel.get_latest_resume_text(app['candidate_id'])
        
        # Calculate Advanced Score
        app['match_score'] = SkillModel.calculate_match_score(
            candidate_skill_ids, 
            job_skill_ids,
            resume_text=resume_text,
            job_description=job['description'],
            job_title=job['title']
        )
        
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