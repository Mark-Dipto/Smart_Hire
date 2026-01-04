"""Resume model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error
from datetime import datetime
import os
import re

# Try importing text extraction libraries
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import docx
except ImportError:
    docx = None

class ResumeModel:
    """Handle resume-related database operations"""
    
    # Expanded Skill Database with Synonyms
    SKILL_DB = {
        'python': ['python', 'py'],
        'javascript': ['javascript', 'js', 'es6', 'node.js', 'nodejs'],
        'java': ['java', 'j2ee', 'spring', 'hibernate'],
        'c++': ['c++', 'cpp', 'c plus plus'],
        'c#': ['c#', 'csharp', '.net', 'dotnet'],
        'sql': ['sql', 'mysql', 'postgresql', 'postgres', 'mssql', 'oracle'],
        'nosql': ['nosql', 'mongodb', 'cassandra', 'redis'],
        'react': ['react', 'reactjs', 'react.js', 'redux'],
        'angular': ['angular', 'angularjs'],
        'vue': ['vue', 'vuejs', 'vue.js'],
        'html': ['html', 'html5'],
        'css': ['css', 'css3', 'sass', 'scss', 'bootstrap', 'tailwind'],
        'flask': ['flask', 'jinja2'],
        'django': ['django', 'drf'],
        'git': ['git', 'github', 'gitlab', 'bitbucket'],
        'docker': ['docker', 'kubernetes', 'k8s', 'containers'],
        'aws': ['aws', 'amazon web services', 'ec2', 's3', 'lambda'],
        'azure': ['azure'],
        'gcp': ['gcp', 'google cloud'],
        'machine learning': ['machine learning', 'ml', 'tensorflow', 'pytorch', 'scikit-learn', 'sklearn', 'pandas', 'numpy'],
        'data analysis': ['data analysis', 'data science', 'tableau', 'power bi'],
        'agile': ['agile', 'scrum', 'kanban', 'jira'],
        'devops': ['devops', 'jenkins', 'ci/cd', 'terraform', 'ansible']
    }

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
    def get_latest_resume_text(candidate_id):
        """Helper to fetch the parsed text of the candidate's latest resume"""
        conn = get_db_connection()
        if not conn:
            return ""
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT parsed_text FROM resumes WHERE candidate_id = %s ORDER BY upload_date DESC LIMIT 1",
                (candidate_id,)
            )
            result = cursor.fetchone()
            conn.close()
            return result['parsed_text'] if result else ""
        except:
            if conn: conn.close()
            return ""

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
        """Extract real text from resume file (PDF/DOCX/TXT)"""
        text = ""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.pdf':
                if PdfReader:
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                else:
                    return "Error: pypdf library not installed. Cannot parse PDF."
            
            elif ext in ['.doc', '.docx']:
                if docx:
                    doc = docx.Document(file_path)
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                else:
                    return "Error: python-docx library not installed. Cannot parse DOCX."
            
            else:
                # Fallback for text files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            
            # Clean text (remove extra whitespace)
            return re.sub(r'\s+', ' ', text).strip()
            
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    @staticmethod
    def extract_skills(text):
        """Extract skills using the Synonym Dictionary"""
        found_skills = set()
        text_lower = text.lower()
        
        # Regex for word boundaries to avoid partial matches (e.g., 'java' inside 'javascript')
        for category, synonyms in ResumeModel.SKILL_DB.items():
            for synonym in synonyms:
                # Escape special characters in synonyms like c++
                pattern = r'\b' + re.escape(synonym) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.add(category) # Add the canonical name (e.g. 'react' even if found 'reactjs')
                    break 
        
        return list(found_skills)