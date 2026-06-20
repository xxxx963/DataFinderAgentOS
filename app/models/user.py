#用户的仓储类，用于管理用户的创建、查询、验证等方法
import hashlib
import secrets
import sqlite3
from app.models.db import get_connection

def _hash_password(password, salt):
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return dk.hex()
class UserRepository:
    @staticmethod
    def create_user(username, password, role_id=None):
        salt_bytes = secrets.token_bytes(16)
        password_hash = _hash_password(password, salt_bytes)
        salt_hex = salt_bytes.hex()

        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash, salt, role_id) VALUES (?, ?, ?, ?)",
                    (username, password_hash, salt_hex, role_id)
                )
                return True
        except sqlite3.IntegrityError:
            return False
    
    @staticmethod
    def get_all(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    """
                    SELECT u.*, r.name as role_name 
                    FROM users u 
                    LEFT JOIN roles r ON u.role_id = r.id 
                    WHERE u.username LIKE ? 
                    ORDER BY u.id DESC LIMIT ? OFFSET ?
                    """,
                    ("%" + keyword + "%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT u.*, r.name as role_name 
                    FROM users u 
                    LEFT JOIN roles r ON u.role_id = r.id 
                    ORDER BY u.id DESC LIMIT ? OFFSET ?
                    """,
                    (page_size, offset)
                )
            return cursor.fetchall()
    
    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT COUNT(*) as count FROM users WHERE username LIKE ?",
                    ("%" + keyword + "%",)
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            return cursor.fetchone()["count"]

    @staticmethod
    def get_user_by_username(username):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, username, password_hash, salt, role_id FROM users WHERE username = ?",
                (username,)
            ).fetchone()
        return row
    
    @staticmethod
    def get_by_id(user_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            return cursor.fetchone()
    
    @staticmethod
    def update_user(user_id, username, role_id=None):
        with get_connection() as conn:
            conn.execute(
                "UPDATE users SET username = ?, role_id = ? WHERE id = ?",
                (username, role_id, user_id)
            )
            conn.commit()
    
    @staticmethod
    def update_password(user_id, password):
        salt_bytes = secrets.token_bytes(16)
        password_hash = _hash_password(password, salt_bytes)
        salt_hex = salt_bytes.hex()
        with get_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
                (password_hash, salt_hex, user_id)
            )
            conn.commit()
    
    @staticmethod
    def delete_user(user_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

    @staticmethod
    def verify_user(username, password):
        row = UserRepository.get_user_by_username(username)
        if not row:
            return False
        salt = bytes.fromhex(row["salt"])
        return _hash_password(password, salt) == row["password_hash"]