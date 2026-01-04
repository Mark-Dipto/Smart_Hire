"""Authentication controller"""
from flask import render_template, request, redirect, url_for, session, flash
from models.user_model import UserModel

def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session

def get_user_role():
    """Get current user role"""
    return session.get('role', None)

def is_candidate():
    """Check if user is a candidate"""
    return get_user_role() == 'candidate'

def is_recruiter():
    """Check if user is a recruiter"""
    return get_user_role() == 'recruiter'

def register_candidate():
    """Handle candidate registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = 'candidate' # Hardcoded for this route
        
        if not all([name, email, password]):
            flash('All fields are required', 'error')
            return render_template('register_candidate.html')
        
        result = UserModel.register(name, email, password, role)
        
        if result['success']:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return render_template('register_candidate.html')
    
    return render_template('register_candidate.html')

def register_recruiter():
    """Handle recruiter registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = 'recruiter' # Hardcoded for this route
        
        if not all([name, email, password]):
            flash('All fields are required', 'error')
            return render_template('register_recruiter.html')
        
        result = UserModel.register(name, email, password, role)
        
        if result['success']:
            flash('Recruiter account created! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return render_template('register_recruiter.html')
    
    return render_template('register_recruiter.html')

def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        result = UserModel.login(email, password)
        
        if result['success']:
            session['user_id'] = result['user_id']
            session['name'] = result['name']
            session['email'] = result['email']
            session['role'] = result['role']
            flash('Login successful!', 'success')
            
            if result['role'] == 'candidate':
                return redirect(url_for('candidate_dashboard'))
            elif result['role'] == 'recruiter':
                return redirect(url_for('recruiter_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash(result['message'], 'error')
    
    return render_template('login.html')

def logout():
    """Handle user logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))