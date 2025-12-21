# Database Configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'database': 'sql12812279',
    'user': 'sql12812279',  # Update with your actual username
    'password': ''  # Update with your actual password
}

# Application Configuration
SECRET_KEY = 'your-secret-key-change-this-in-production'
UPLOAD_FOLDER = 'uploads/resumes'
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

