"""Application model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error

class ApplicationModel:
    """Handle application-related database operations"""
    
    @staticmethod
    def create_application(job_id, candidate_id):
        """Submit a new application"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO applications (job_id, candidate_id, status) VALUES (%s, %s, 'pending')",
                (job_id, candidate_id)
            )
            conn.commit()
            conn.close()
            return {'success': True}
        except Error as e:
            if conn:
                conn.close()
            # Check for duplicate entry
            if e.errno == 1062:
                return {'success': False, 'message': 'You have already applied for this job'}
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_applications_by_job(job_id):
        """Get all applications for a specific job with candidate details"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, u.name, u.email,
                       (SELECT file_path FROM resumes r WHERE r.candidate_id = u.user_id ORDER BY upload_date DESC LIMIT 1) as resume_path
                FROM applications a
                JOIN users u ON a.candidate_id = u.user_id
                WHERE a.job_id = %s
                ORDER BY a.applied_at DESC
            """, (job_id,))
            apps = cursor.fetchall()
            conn.close()
            return apps
        except Error as e:
            if conn:
                conn.close()
            return []

    @staticmethod
    def get_applications_by_candidate(candidate_id):
        """Get all applications made by a candidate"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.*, j.title, j.location, j.recruiter_id
                FROM applications a
                JOIN jobs j ON a.job_id = j.job_id
                WHERE a.candidate_id = %s
                ORDER BY a.applied_at DESC
            """, (candidate_id,))
            apps = cursor.fetchall()
            conn.close()
            return apps
        except Error as e:
            if conn:
                conn.close()
            return []

    @staticmethod
    def update_status(application_id, status):
        """Update application status (accepted/rejected)"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE applications SET status = %s WHERE application_id = %s",
                (status, application_id)
            )
            conn.commit()
            conn.close()
            return {'success': True}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': str(e)}
            
    @staticmethod
    def has_applied(candidate_id, job_id):
        """Check if candidate has already applied"""
        conn = get_db_connection()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM applications WHERE candidate_id = %s AND job_id = %s",
                (candidate_id, job_id)
            )
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except Error:
            if conn: conn.close()
            return False