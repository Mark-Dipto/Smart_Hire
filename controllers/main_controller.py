"""Main controller for home page"""
from flask import render_template, redirect, url_for, session
from controllers.auth_controller import is_logged_in

def index():
    """Home page route"""
    if is_logged_in():
        role = session.get('role', None)
        if role == 'candidate':
            return redirect(url_for('candidate_dashboard'))
        elif role == 'recruiter':
            return redirect(url_for('recruiter_dashboard'))
    return render_template('index.html')

