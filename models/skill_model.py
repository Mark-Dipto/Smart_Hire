"""Skill model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error

class SkillModel:
    """Handle skill-related database operations"""
    
    @staticmethod
    def get_or_create_skill(skill_name):
        """Get skill ID or create if doesn't exist"""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT skill_id FROM skills WHERE name = %s", (skill_name,))
            skill = cursor.fetchone()
            
            if not skill:
                cursor.execute("INSERT INTO skills (name) VALUES (%s)", (skill_name,))
                skill_id = cursor.lastrowid
                conn.commit()
            else:
                skill_id = skill[0]
            
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
                "SELECT s.skill_id, s.name FROM candidate_skills cs JOIN skills s ON cs.skill_id = s.skill_id WHERE cs.candidate_id = %s",
                (candidate_id,)
            )
            skills = {row['skill_id']: row['name'] for row in cursor.fetchall()}
            conn.close()
            return skills
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
                "SELECT s.skill_id, s.name FROM job_skills js JOIN skills s ON js.skill_id = s.skill_id WHERE js.job_id = %s",
                (job_id,)
            )
            skills = {row['skill_id']: row['name'] for row in cursor.fetchall()}
            conn.close()
            return skills
        except Error as e:
            if conn:
                conn.close()
            return {}
    
    @staticmethod
    def get_all_candidates_with_resumes():
        """Get all candidates who have uploaded resumes"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT DISTINCT c.candidate_id, u.name, u.email FROM candidates c JOIN users u ON c.candidate_id = u.user_id JOIN resumes r ON c.candidate_id = r.candidate_id"
            )
            candidates = cursor.fetchall()
            conn.close()
            return candidates
        except Error as e:
            if conn:
                conn.close()
            return []
    
    @staticmethod
    def calculate_match_score(candidate_skill_ids, job_skill_ids):
        """Calculate match score between candidate and job"""
        if len(job_skill_ids) == 0:
            return 0
        
        matching_skills = candidate_skill_ids.intersection(job_skill_ids)
        match_score = (len(matching_skills) / len(job_skill_ids)) * 100
        return round(match_score, 2)

