"""User model for database operations"""
from models.database import get_db_connection
from mysql.connector import Error
import hashlib

class UserModel:
    """Handle user-related database operations"""

    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register(name, email, password, role):
        """Register a new user"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}

        try:
            cursor = conn.cursor()
            hashed_password = UserModel.hash_password(password)
            
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                (name, email, hashed_password, role)
            )
            conn.commit()
            conn.close()
            return {'success': True, 'message': 'User registered successfully'}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Registration failed: {str(e)}'}

    @staticmethod
    def login(email, password):
        """Authenticate user login"""
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'message': 'Database connection error'}

        try:
            cursor = conn.cursor(dictionary=True)
            hashed_password = UserModel.hash_password(password)
            
            cursor.execute(
                "SELECT user_id, name, email, role FROM users WHERE email = %s AND password = %s",
                (email, hashed_password)
            )
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'success': True,
                    'user_id': user['user_id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role']
                }
            else:
                return {'success': False, 'message': 'Invalid email or password'}
        except Error as e:
            if conn:
                conn.close()
            return {'success': False, 'message': f'Login failed: {str(e)}'}

    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            conn.close()
            return user
        except Error as e:
            if conn:
                conn.close()
            return None
