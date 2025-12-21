"""Resume model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error
from datetime import datetime

class ResumeModel:
    """Handle resume-related database operations"""
    
    @staticmethod
    def get_resumes_by_candidate(candidate_id):
        """Get all resumes for a candidate"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM resumes WHERE candidate_id = %s ORDER BY upload_date DESC",
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
    def save_resume(candidate_id, file_path, parsed_text):
        """Save resume to database"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO resumes (candidate_id, file_path, upload_date, parsed_text) VALUES (%s, %s, %s, %s)",
                (candidate_id, file_path, datetime.now().date(), parsed_text)
            )
            resume_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return {'success': True, 'resume_id': resume_id}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Error saving resume: {str(e)}'}
    
    @staticmethod
    def extract_text_from_resume(file_path):
        """Extract text from resume file"""
        try:
            if file_path.endswith('.pdf'):
                # For PDF files, return sample text for demo
                # In production, use PyPDF2: pip install PyPDF2
                return "Resume content with skills: Python, JavaScript, SQL, Flask, MySQL, React, HTML, CSS, Git, Docker"
            elif file_path.endswith(('.doc', '.docx')):
                # For Word documents, use python-docx: pip install python-docx
                return "Resume content with skills: Python, JavaScript, SQL, Flask, MySQL, React, HTML, CSS, Git, Docker"
            else:
                # For text files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    @staticmethod
    def extract_skills(text):
        """Extract skills from resume text"""
        common_skills = [
            'python', 'javascript', 'java', 'c++', 'sql', 'mysql', 'flask', 'django',
            'react', 'angular', 'vue', 'html', 'css', 'php', 'node.js', 'mongodb',
            'postgresql', 'git', 'docker', 'aws', 'linux', 'agile', 'scrum'
        ]
        text_lower = text.lower()
        found_skills = [skill for skill in common_skills if skill in text_lower]
        return found_skills

