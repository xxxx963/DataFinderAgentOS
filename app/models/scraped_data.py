import sqlite3
from app.models.db import get_connection

class ScrapedDataRepository:
    @staticmethod
    def get_all(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    """
                    SELECT sd.*, ss.name as source_name 
                    FROM scraped_data sd
                    LEFT JOIN scraping_sources ss ON sd.source_id = ss.id
                    WHERE sd.title LIKE ? OR sd.url LIKE ? OR sd.summary LIKE ? OR ss.name LIKE ?
                    ORDER BY sd.id DESC LIMIT ? OFFSET ?
                    """,
                    ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    """
                    SELECT sd.*, ss.name as source_name 
                    FROM scraped_data sd
                    LEFT JOIN scraping_sources ss ON sd.source_id = ss.id
                    ORDER BY sd.id DESC LIMIT ? OFFSET ?
                    """,
                    (page_size, offset)
                )
            return cursor.fetchall()

    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    """
                    SELECT COUNT(sd.id) as count 
                    FROM scraped_data sd
                    LEFT JOIN scraping_sources ss ON sd.source_id = ss.id
                    WHERE sd.title LIKE ? OR sd.url LIKE ? OR sd.summary LIKE ? OR ss.name LIKE ?
                    """,
                    ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%",)
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM scraped_data")
            return cursor.fetchone()["count"]

    @staticmethod
    def get_by_id(data_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM scraped_data WHERE id = ?", (data_id,))
            return cursor.fetchone()

    @staticmethod
    def delete_data(data_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM scraped_data WHERE id = ?", (data_id,))
            conn.commit()

    @staticmethod
    def delete_multiple_data(data_ids):
        with get_connection() as conn:
            # Create a placeholder string for the IN clause (e.g., '?,?,?')
            placeholders = ', '.join('?' for _ in data_ids)
            conn.execute(f"DELETE FROM scraped_data WHERE id IN ({placeholders})", data_ids)
            conn.commit()
