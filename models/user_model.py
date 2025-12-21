"""User model for database operations"""
import hashlib
from models.database import get_db_connection
from mysql.connector import Error

class UserModel:
    """Handle user-related database operations"""
    
    @staticmethod
    def register(name, email, password, role):
        """Register a new user"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                conn.close()
                return {'success': False, 'message': 'Email already registered'}
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Insert user
            cursor.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (name, email, password_hash, role)
            )
            user_id = cursor.lastrowid
            
            # Insert into role-specific table
            if role == 'candidate':
                cursor.execute("INSERT INTO candidates (candidate_id) VALUES (%s)", (user_id,))
            elif role == 'recruiter':
                cursor.execute("INSERT INTO recruiters (recruiter_id) VALUES (%s)", (user_id,))
            elif role == 'admin':
                cursor.execute("INSERT INTO admins (admin_id) VALUES (%s)", (user_id,))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'user_id': user_id}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Registration error: {str(e)}'}
    
    @staticmethod
    def login(email, password):
        """Authenticate user login"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, name, email, password_hash, role FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()
            conn.close()
            
            if user and hashlib.sha256(password.encode()).hexdigest() == user['password_hash']:
                return {
                    'success': True,
                    'user_id': user['user_id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            
            return {'success': False, 'message': 'Invalid email or password'}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Login error: {str(e)}'}
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, name, email, role, created_at FROM users WHERE user_id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            conn.close()
            return user
        except Error as e:
            if conn:
                conn.close()
            return None

