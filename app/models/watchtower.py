import sqlite3
from app.models.db import get_connection

class WatchtowerSourceRepository:
    @staticmethod
    def create_source(name, url, request_headers, method='GET', enabled=1, description=''):
        try:
            with get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO scraping_sources (name, url, request_headers, method, enabled, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (name, url, request_headers, method, enabled, description)
                )
                conn.commit()
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
                    SELECT * FROM scraping_sources 
                    WHERE name LIKE ? OR url LIKE ? OR description LIKE ?
                    ORDER BY id DESC LIMIT ? OFFSET ?
                    """,
                    ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT * FROM scraping_sources 
                    ORDER BY id DESC LIMIT ? OFFSET ?
                    """,
                    (page_size, offset)
                )
            return cursor.fetchall()

    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT COUNT(*) as count FROM scraping_sources WHERE name LIKE ? OR url LIKE ? OR description LIKE ?",
                    ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%",)
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM scraping_sources")
            return cursor.fetchone()["count"]

    @staticmethod
    def get_by_id(source_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM scraping_sources WHERE id = ?", (source_id,))
            return cursor.fetchone()

    @staticmethod
    def update_source(source_id, name, url, request_headers, method, enabled, description):
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE scraping_sources 
                SET name = ?, url = ?, request_headers = ?, method = ?, enabled = ?, description = ?
                WHERE id = ?
                """,
                (name, url, request_headers, method, enabled, description, source_id)
            )
            conn.commit()

    @staticmethod
    def delete_source(source_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM scraping_sources WHERE id = ?", (source_id,))
            conn.commit()
