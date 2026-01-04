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
            if e.errno == 1062:
                return {'success': False, 'message': 'You have already applied for this job'}
            return {'success': False, 'message': str(e)}

    @staticmethod
    def offer_job(job_id, candidate_id):
        """Offer a job to a candidate (Sets status to 'offered')"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            cursor = conn.cursor()
            # Check if exists first
            cursor.execute(
                "SELECT application_id FROM applications WHERE job_id = %s AND candidate_id = %s",
                (job_id, candidate_id)
            )
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute(
                    "UPDATE applications SET status = 'offered' WHERE application_id = %s",
                    (existing[0],)
                )
            else:
                cursor.execute(
                    "INSERT INTO applications (job_id, candidate_id, status) VALUES (%s, %s, 'offered')",
                    (job_id, candidate_id)
                )
                
            conn.commit()
            conn.close()
            return {'success': True}
        except Error as e:
            if conn: conn.close()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def respond_to_offer(application_id, status):
        """Candidate accepts or rejects an offer"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            if status not in ['accepted', 'rejected']:
                return {'success': False, 'message': 'Invalid status'}

            cursor = conn.cursor()
            # Verify it's currently 'offered'
            cursor.execute("SELECT status FROM applications WHERE application_id = %s", (application_id,))
            result = cursor.fetchone()
            
            if not result or result[0] != 'offered':
                 conn.close()
                 return {'success': False, 'message': 'This offer is no longer valid'}

            cursor.execute(
                "UPDATE applications SET status = %s WHERE application_id = %s",
                (status, application_id)
            )
            conn.commit()
            conn.close()
            return {'success': True}
        except Error as e:
            if conn: conn.close()
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_applications_by_job(job_id):
        """Get all applications for a specific job"""
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
                ORDER BY FIELD(a.status, 'pending', 'offered', 'accepted', 'rejected'), a.applied_at DESC
            """, (job_id,))
            apps = cursor.fetchall()
            conn.close()
            return apps
        except Error as e:
            if conn: conn.close()
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
            if conn: conn.close()
            return []

    @staticmethod
    def update_status(application_id, status):
        """Update application status (generic)"""
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
            if conn: conn.close()
            return {'success': False, 'message': str(e)}
            
    @staticmethod
    def has_applied(candidate_id, job_id):
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM applications WHERE candidate_id = %s AND job_id = %s", (candidate_id, job_id))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except Error:
            if conn: conn.close()
            return False