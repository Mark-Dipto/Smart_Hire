"""Skill model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error
import re

class SkillModel:
    """Handle skill-related database operations"""
    
    @staticmethod
    def get_or_create_skill(skill_name):
        """Get skill ID or create if doesn't exist"""
        conn = get_db_connection()
        if not conn: return None
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
        except Error:
            if conn: conn.close()
            return None
    
    @staticmethod
    def link_skill_to_candidate(candidate_id, skill_id):
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT IGNORE INTO candidate_skills (candidate_id, skill_id) VALUES (%s, %s)", (candidate_id, skill_id))
            conn.commit()
            conn.close()
            return True
        except Error:
            if conn: conn.close()
            return False
    
    @staticmethod
    def link_skill_to_job(job_id, skill_id):
        conn = get_db_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT IGNORE INTO job_skills (job_id, skill_id) VALUES (%s, %s)", (job_id, skill_id))
            conn.commit()
            conn.close()
            return True
        except Error:
            if conn: conn.close()
            return False
    
    @staticmethod
    def get_candidate_skills(candidate_id):
        conn = get_db_connection()
        if not conn: return {}
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT s.skill_id, s.name FROM candidate_skills cs JOIN skills s ON cs.skill_id = s.skill_id WHERE cs.candidate_id = %s", (candidate_id,))
            skills = {row['skill_id']: row['name'] for row in cursor.fetchall()}
            conn.close()
            return skills
        except Error:
            if conn: conn.close()
            return {}
    
    @staticmethod
    def get_job_skills(job_id):
        conn = get_db_connection()
        if not conn: return {}
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT s.skill_id, s.name FROM job_skills js JOIN skills s ON js.skill_id = s.skill_id WHERE js.job_id = %s", (job_id,))
            skills = {row['skill_id']: row['name'] for row in cursor.fetchall()}
            conn.close()
            return skills
        except Error:
            if conn: conn.close()
            return {}

    @staticmethod
    def get_all_candidates_with_resumes():
        conn = get_db_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT c.candidate_id, u.name, u.email FROM candidates c JOIN users u ON c.candidate_id = u.user_id JOIN resumes r ON c.candidate_id = r.candidate_id")
            candidates = cursor.fetchall()
            conn.close()
            return candidates
        except Error:
            if conn: conn.close()
            return []

    # --- ADVANCED AI MATCHING ---
    
    @staticmethod
    def calculate_match_score(candidate_skill_ids, job_skill_ids, resume_text="", job_description="", job_title=""):
        """
        Calculate Advanced Match Score (0-100)
        
        Components:
        1. Skill Overlap (70%): Direct match of tagged skills.
        2. Context Match (30%): Semantic relevance of resume text to job description.
        3. Title Boost (+10%): If resume contains the exact Job Title.
        """
        
        # 1. Skill Score (Weight: 70%)
        skill_score = 0
        if len(job_skill_ids) > 0:
            matching_skills = candidate_skill_ids.intersection(job_skill_ids)
            skill_score = (len(matching_skills) / len(job_skill_ids)) * 100
        else:
            # If no skills required, assume 50% base skill match
            skill_score = 50

        # 2. Context Score (Weight: 30%)
        context_score = 0
        if resume_text and job_description:
            # Normalize text
            r_text = resume_text.lower()
            j_text = job_description.lower()
            
            # Extract Keywords from Job Description (simple extraction of words > 4 chars)
            job_keywords = set(re.findall(r'\b\w{4,}\b', j_text))
            
            # Count how many job keywords appear in resume
            matches = sum(1 for word in job_keywords if word in r_text)
            
            if len(job_keywords) > 0:
                context_score = (matches / len(job_keywords)) * 100
        
        # 3. Calculate Weighted Average
        final_score = (skill_score * 0.7) + (context_score * 0.3)
        
        # 4. Title Boost
        if job_title and resume_text:
            if job_title.lower() in resume_text.lower():
                final_score += 10
        
        # Cap at 100
        return min(round(final_score, 0), 100)