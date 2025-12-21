"""Main application entry point"""
from flask import Flask
import os
from config import SECRET_KEY, UPLOAD_FOLDER, MAX_CONTENT_LENGTH

# Import controllers
from controllers.main_controller import index
from controllers.auth_controller import register, login, logout
from controllers.candidate_controller import candidate_dashboard, upload_resume, candidate_matches
from controllers.recruiter_controller import recruiter_dashboard, create_job, job_matches

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Add cache control headers
@app.after_request
def set_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Register routes
# Main routes
app.add_url_rule('/', 'index', index, methods=['GET'])

# Authentication routes
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['GET'])

# Candidate routes
app.add_url_rule('/candidate/dashboard', 'candidate_dashboard', candidate_dashboard, methods=['GET'])
app.add_url_rule('/candidate/upload_resume', 'upload_resume', upload_resume, methods=['GET', 'POST'])
app.add_url_rule('/candidate/matches', 'candidate_matches', candidate_matches, methods=['GET'])

# Recruiter routes
app.add_url_rule('/recruiter/dashboard', 'recruiter_dashboard', recruiter_dashboard, methods=['GET'])
app.add_url_rule('/recruiter/create_job', 'create_job', create_job, methods=['GET', 'POST'])
app.add_url_rule('/recruiter/job/<int:job_id>/matches', 'job_matches', job_matches, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
