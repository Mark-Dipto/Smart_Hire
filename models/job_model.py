"""Job model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error
from datetime import datetime

class JobModel:
    """Handle job-related database operations"""
    
    @staticmethod
    def get_jobs_by_recruiter(recruiter_id):
        """Get all jobs for a recruiter"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM jobs WHERE recruiter_id = %s ORDER BY created_at DESC",
                (recruiter_id,)
            )
            jobs = cursor.fetchall()
            conn.close()
            return jobs
        except Error as e:
            if conn:
                conn.close()
            return []
    
    @staticmethod
    def get_active_jobs():
        """Get all active jobs"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM jobs WHERE is_active = 1")
            jobs = cursor.fetchall()
            conn.close()
            return jobs
        except Error as e:
            if conn:
                conn.close()
            return []
    
    @staticmethod
    def get_job_by_id(job_id, recruiter_id=None):
        """Get job by ID, optionally verify recruiter ownership"""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            if recruiter_id:
                cursor.execute(
                    "SELECT * FROM jobs WHERE job_id = %s AND recruiter_id = %s",
                    (job_id, recruiter_id)
                )
            else:
                cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
            job = cursor.fetchone()
            conn.close()
            return job
        except Error as e:
            if conn:
                conn.close()
            return None
    
    @staticmethod
    def create_job(recruiter_id, title, description, location):
        """Create a new job posting"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO jobs (recruiter_id, title, description, location, created_at, is_active) VALUES (%s, %s, %s, %s, %s, %s)",
                (recruiter_id, title, description, location, datetime.now().date(), 1)
            )
            job_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return {'success': True, 'job_id': job_id}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error creating job: {str(e)}'}

