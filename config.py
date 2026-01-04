# Database Configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'database': 'sql12813337',
    'user': 'sql12813337',  # Update with your actual username
    'password': 'QaPLB39FdB'
}

# Application Configuration
SECRET_KEY = 'your-secret-key-change-this-in-production'
UPLOAD_FOLDER = 'uploads/resumes'
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
