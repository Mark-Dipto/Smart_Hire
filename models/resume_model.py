"""Resume model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error
import os

class ResumeModel:
    """Handle resume-related database operations"""

    @staticmethod
    def extract_text_from_resume(file_path):
        """Extract text from resume file"""
        text = ""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except:
            text = ""
        return text

    @staticmethod
    def extract_skills(text):
        """Extract skills from resume text"""
        common_skills = [
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'sql', 'mysql', 'mongodb', 'postgresql', 'redis',
            'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'django', 'flask',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'agile', 'scrum', 'rest api', 'graphql'
        ]
        
        text_lower = text.lower()
        found_skills = set()
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.add(skill)
        
        return list(found_skills)

    @staticmethod
    def save_resume(user_id, file_path, parsed_text):
        """Save resume to database"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO resumes (candidate_id, file_path, parsed_text) VALUES (%s, %s, %s)",
                (user_id, file_path, parsed_text)
            )
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'Resume saved successfully'}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error saving resume: {str(e)}'}

    @staticmethod
    def get_resumes_by_candidate(candidate_id):
        """Get all resumes for a candidate"""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM resumes WHERE candidate_id = %s ORDER BY uploaded_at DESC",
                (candidate_id,)
            )
            resumes = cursor.fetchall()
            conn.close()
            return resumes
        except Error as e:
            if conn:
                conn.close()
            return []

    @staticmethod
    def delete_resume(resume_id, candidate_id):
        """Delete a resume"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT file_path FROM resumes WHERE resume_id = %s AND candidate_id = %s",
                (resume_id, candidate_id)
            )
            resume = cursor.fetchone()
            
            if resume and os.path.exists(resume['file_path']):
                os.remove(resume['file_path'])
            
            cursor.execute(
                "DELETE FROM resumes WHERE resume_id = %s AND candidate_id = %s",
                (resume_id, candidate_id)
            )
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'Resume deleted successfully'}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error deleting resume: {str(e)}'}
