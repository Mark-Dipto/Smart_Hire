"""Skill model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error

class SkillModel:
    """Handle skill-related database operations"""

    @staticmethod
    def get_or_create_skill(skill_name):
        """Get skill by name or create if doesn't exist"""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            skill_name_lower = skill_name.lower().strip()
            
            cursor.execute(
                "SELECT skill_id FROM skills WHERE LOWER(skill_name) = %s",
                (skill_name_lower,)
            )
            skill = cursor.fetchone()
            
            if skill:
                conn.close()
                return skill['skill_id']
            
            cursor.execute(
                "INSERT INTO skills (skill_name) VALUES (%s)",
                (skill_name,)
            )
            skill_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return skill_id
        except Error as e:
            if conn:
                conn.close()
            return None

    @staticmethod
    def link_skill_to_candidate(candidate_id, skill_id):
        """Link a skill to a candidate"""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT IGNORE INTO candidate_skills (candidate_id, skill_id) VALUES (%s, %s)",
                (candidate_id, skill_id)
            )
            conn.commit()
            conn.close()
            return True
        except Error as e:
            if conn:
                conn.close()
            return False

    @staticmethod
    def link_skill_to_job(job_id, skill_id):
        """Link a skill to a job"""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT IGNORE INTO job_skills (job_id, skill_id) VALUES (%s, %s)",
                (job_id, skill_id)
            )
            conn.commit()
            conn.close()
            return True
        except Error as e:
            if conn:
                conn.close()
            return False

    @staticmethod
    def get_candidate_skills(candidate_id):
        """Get all skills for a candidate"""
        conn = get_db_connection()
        if not conn:
            return {}

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT s.skill_id, s.skill_name 
                   FROM skills s 
                   JOIN candidate_skills cs ON s.skill_id = cs.skill_id 
                   WHERE cs.candidate_id = %s""",
                (candidate_id,)
            )
            skills = cursor.fetchall()
            conn.close()
            
            skill_dict = {}
            for skill in skills:
                skill_dict[skill['skill_id']] = skill['skill_name']
            return skill_dict
        except Error as e:
            if conn:
                conn.close()
            return {}

    @staticmethod
    def get_job_skills(job_id):
        """Get all skills for a job"""
        conn = get_db_connection()
        if not conn:
            return {}

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT s.skill_id, s.skill_name 
                   FROM skills s 
                   JOIN job_skills js ON s.skill_id = js.skill_id 
                   WHERE js.job_id = %s""",
                (job_id,)
            )
            skills = cursor.fetchall()
            conn.close()
            
            skill_dict = {}
            for skill in skills:
                skill_dict[skill['skill_id']] = skill['skill_name']
            return skill_dict
        except Error as e:
            if conn:
                conn.close()
            return {}

    @staticmethod
    def get_all_candidates_with_resumes():
        """Get all candidates that have uploaded resumes"""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT DISTINCT u.user_id as candidate_id, u.name, u.email, COUNT(r.resume_id) as resume_count
                   FROM users u 
                   JOIN resumes r ON u.user_id = r.candidate_id 
                   WHERE u.role = 'candidate'
                   GROUP BY u.user_id, u.name, u.email"""
            )
            candidates = cursor.fetchall()
            conn.close()
            return candidates
        except Error as e:
            if conn:
                conn.close()
            return []

    @staticmethod
    def calculate_match_score(candidate_skills, job_skills):
        """Calculate match score between candidate and job skills"""
        if not job_skills:
            return 0
        
        matching = len(candidate_skills.intersection(job_skills))
        total_required = len(job_skills)
        
        return round((matching / total_required) * 100, 2) if total_required > 0 else 0
