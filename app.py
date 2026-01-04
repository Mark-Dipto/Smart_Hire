"""Main application entry point"""
from flask import Flask
import os
from config import SECRET_KEY, UPLOAD_FOLDER, MAX_CONTENT_LENGTH

# Import controllers
from controllers.main_controller import index, careers, recruiter_landing, download_resume
from controllers.auth_controller import register_candidate, register_recruiter, login, logout
from controllers.candidate_controller import candidate_dashboard, upload_resume, apply_job, respond_to_offer
from controllers.recruiter_controller import recruiter_dashboard, create_job, job_matches, job_applications, update_application_status, offer_job

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.after_request
def set_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# --- Routes ---
app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/careers', 'careers', careers, methods=['GET'])
app.add_url_rule('/recruiters', 'recruiter_landing', recruiter_landing, methods=['GET'])
app.add_url_rule('/uploads/resumes/<filename>', 'download_resume', download_resume, methods=['GET'])

app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/register', 'register_candidate', register_candidate, methods=['GET', 'POST']) 
app.add_url_rule('/register/recruiter', 'register_recruiter', register_recruiter, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['GET'])

app.add_url_rule('/candidate/dashboard', 'candidate_dashboard', candidate_dashboard, methods=['GET'])
app.add_url_rule('/candidate/upload_resume', 'upload_resume', upload_resume, methods=['GET', 'POST'])
app.add_url_rule('/candidate/apply/<int:job_id>', 'apply_job', apply_job, methods=['POST'])
app.add_url_rule('/candidate/offer/<int:application_id>/<status>', 'respond_to_offer', respond_to_offer, methods=['GET']) # New Route

app.add_url_rule('/recruiter/dashboard', 'recruiter_dashboard', recruiter_dashboard, methods=['GET'])
app.add_url_rule('/recruiter/create_job', 'create_job', create_job, methods=['GET', 'POST'])
app.add_url_rule('/recruiter/job/<int:job_id>/matches', 'job_matches', job_matches, methods=['GET'])
app.add_url_rule('/recruiter/job/<int:job_id>/applications', 'job_applications', job_applications, methods=['GET'])
app.add_url_rule('/recruiter/application/<int:application_id>/update', 'update_application_status', update_application_status, methods=['POST'])
app.add_url_rule('/recruiter/job/<int:job_id>/offer/<int:candidate_id>', 'offer_job', offer_job, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3306)