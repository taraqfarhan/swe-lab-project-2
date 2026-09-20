from werkzeug.security import generate_password_hash, check_password_hash
from src.database.db import query_db, execute_db
from src.models.user import User

class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str, role: str, full_name: str, phone: str = '', address: str = ''):
        """Register a new user in the system."""
        # Check if username or email already exists
        existing = query_db(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            (username.strip().lower(), email.strip().lower()),
            one=True
        )
        if existing:
            return None, "Username or Email is already registered."

        if role not in ('customer', 'restaurant_owner', 'rider', 'admin'):
            role = 'customer'

        password_hash = generate_password_hash(password)
        user_id = execute_db(
            """INSERT INTO users (username, email, password_hash, role, full_name, phone, address)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (username.strip().lower(), email.strip().lower(), password_hash, role, full_name.strip(), phone.strip(), address.strip())
        )
        user_data = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
        return User.from_dict(user_data), None

    @staticmethod
    def authenticate_user(username_or_email: str, password: str):
        """Authenticate a user by username or email and return User instance if valid."""
        identifier = username_or_email.strip().lower()
        user_data = query_db(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (identifier, identifier),
            one=True
        )
        if not user_data:
            return None, "Invalid username/email or password."

        if not check_password_hash(user_data['password_hash'], password):
            return None, "Invalid username/email or password."

        return User.from_dict(user_data), None

    @staticmethod
    def get_user_by_id(user_id: int):
        user_data = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
        return User.from_dict(user_data) if user_data else None

    @staticmethod
    def get_all_users():
        rows = query_db("SELECT id, username, email, role, full_name, phone, address, created_at FROM users ORDER BY id ASC")
        return [User.from_dict(r) for r in rows]
