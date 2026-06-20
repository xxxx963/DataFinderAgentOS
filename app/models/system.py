
from app.models.db import get_connection


class RoleRepository:
    @staticmethod
    def get_all(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT * FROM roles WHERE name LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM roles ORDER BY id DESC LIMIT ? OFFSET ?",
                    (page_size, offset)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT COUNT(*) as count FROM roles WHERE name LIKE ?",
                    (f"%{keyword}%",)
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM roles")
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(role_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM roles WHERE id = ?", (role_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create(name, description="", is_default=0):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO roles (name, description, is_default) VALUES (?, ?, ?)",
                (name, description, is_default)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update(role_id, name, description):
        with get_connection() as conn:
            conn.execute(
                "UPDATE roles SET name = ?, description = ? WHERE id = ?",
                (name, description, role_id)
            )
            conn.commit()
    
    @staticmethod
    def delete(role_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM role_functions WHERE role_id = ?", (role_id,))
            conn.execute("DELETE FROM roles WHERE id = ?", (role_id,))
            conn.commit()
    
    @staticmethod
    def set_role_functions(role_id, function_ids):
        with get_connection() as conn:
            conn.execute("DELETE FROM role_functions WHERE role_id = ?", (role_id,))
            for func_id in function_ids:
                conn.execute(
                    "INSERT INTO role_functions (role_id, function_id) VALUES (?, ?)",
                    (role_id, func_id)
                )
            conn.commit()
    
    @staticmethod
    def get_role_functions(role_id):
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT function_id FROM role_functions WHERE role_id = ?",
                (role_id,)
            )
            return [row["function_id"] for row in cursor.fetchall()]


class FunctionRepository:
    @staticmethod
    def get_all(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT * FROM functions WHERE name LIKE ? ORDER BY sort_order ASC, id ASC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM functions ORDER BY sort_order ASC, id ASC LIMIT ? OFFSET ?",
                    (page_size, offset)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT COUNT(*) as count FROM functions WHERE name LIKE ?",
                    (f"%{keyword}%",)
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM functions")
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(func_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM functions WHERE id = ?", (func_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_all_tree():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM functions ORDER BY sort_order ASC, id ASC")
            all_funcs = cursor.fetchall()
        return all_funcs
    
    @staticmethod
    def create(name, icon, path, parent_id=0, sort_order=0):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO functions (name, icon, path, parent_id, sort_order) VALUES (?, ?, ?, ?, ?)",
                (name, icon, path, parent_id, sort_order)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update(func_id, name, icon, path, parent_id, sort_order):
        with get_connection() as conn:
            conn.execute(
                "UPDATE functions SET name = ?, icon = ?, path = ?, parent_id = ?, sort_order = ? WHERE id = ?",
                (name, icon, path, parent_id, sort_order, func_id)
            )
            conn.commit()
    
    @staticmethod
    def delete(func_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM role_functions WHERE function_id = ?", (func_id,))
            conn.execute("DELETE FROM functions WHERE id = ?", (func_id,))
            conn.commit()


class ModelEngineRepository:
    @staticmethod
    def get_all(page=1, page_size=6, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT * FROM model_engines WHERE name LIKE ? OR model_name LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", f"%{keyword}%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM model_engines ORDER BY id DESC LIMIT ? OFFSET ?",
                    (page_size, offset)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT COUNT(*) as count FROM model_engines WHERE name LIKE ? OR model_name LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%")
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM model_engines")
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(model_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM model_engines WHERE id = ?", (model_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_default():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM model_engines WHERE is_default = 1 LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create(name, model_name, api_key, base_url, model_type='text', 
               temperature=0.7, max_tokens=2048, top_p=1.0, system_prompt='', 
               is_default=0, enable_sse=0, enable_think=0):
        with get_connection() as conn:
            if is_default:
                conn.execute("UPDATE model_engines SET is_default = 0")
            cursor = conn.execute(
                """INSERT INTO model_engines 
                   (name, model_name, api_key, base_url, model_type, temperature, 
                    max_tokens, top_p, system_prompt, is_default, enable_sse, enable_think) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, model_name, api_key, base_url, model_type, temperature, 
                 max_tokens, top_p, system_prompt, is_default, enable_sse, enable_think)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update(model_id, name, model_name, api_key, base_url, model_type, 
               temperature, max_tokens, top_p, system_prompt, is_default, 
               enable_sse, enable_think):
        with get_connection() as conn:
            if is_default:
                conn.execute("UPDATE model_engines SET is_default = 0 WHERE id != ?", (model_id,))
            conn.execute(
                """UPDATE model_engines 
                   SET name = ?, model_name = ?, api_key = ?, base_url = ?, 
                       model_type = ?, temperature = ?, max_tokens = ?, 
                       top_p = ?, system_prompt = ?, is_default = ?, 
                       enable_sse = ?, enable_think = ?
                   WHERE id = ?""",
                (name, model_name, api_key, base_url, model_type, temperature, 
                 max_tokens, top_p, system_prompt, is_default, enable_sse, 
                 enable_think, model_id)
            )
            conn.commit()
    
    @staticmethod
    def delete(model_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM model_engines WHERE id = ?", (model_id,))
            conn.commit()
    
    @staticmethod
    def update_token_count(model_id, token_count):
        with get_connection() as conn:
            conn.execute("UPDATE model_engines SET token_count = token_count + ? WHERE id = ?", (token_count, model_id))
            conn.commit()
    
    @staticmethod
    def set_default(model_id):
        with get_connection() as conn:
            conn.execute("UPDATE model_engines SET is_default = 0")
            conn.execute("UPDATE model_engines SET is_default = 1 WHERE id = ?", (model_id,))
            conn.commit()


class ScrapingSourceRepository:
    @staticmethod
    def get_all(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT * FROM scraping_sources WHERE name LIKE ? OR url LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", f"%{keyword}%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM scraping_sources ORDER BY id DESC LIMIT ? OFFSET ?",
                    (page_size, offset)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT COUNT(*) as count FROM scraping_sources WHERE name LIKE ? OR url LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%")
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM scraping_sources")
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(source_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM scraping_sources WHERE id = ?", (source_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create(name, url, request_headers, method='GET', enabled=1, description=''):
        import json
        headers_json = json.dumps(request_headers) if isinstance(request_headers, dict) else request_headers
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO scraping_sources (name, url, request_headers, method, enabled, description) VALUES (?, ?, ?, ?, ?, ?)",
                (name, url, headers_json, method, enabled, description)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update(source_id, name, url, request_headers, method, enabled, description):
        import json
        headers_json = json.dumps(request_headers) if isinstance(request_headers, dict) else request_headers
        with get_connection() as conn:
            conn.execute(
                "UPDATE scraping_sources SET name = ?, url = ?, request_headers = ?, method = ?, enabled = ?, description = ? WHERE id = ?",
                (name, url, headers_json, method, enabled, description, source_id)
            )
            conn.commit()
    
    @staticmethod
    def delete(source_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM scraped_data WHERE source_id = ?", (source_id,))
            conn.execute("DELETE FROM scraping_sources WHERE id = ?", (source_id,))
            conn.commit()
    
    @staticmethod
    def get_enabled_sources():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM scraping_sources WHERE enabled = 1")
            return [dict(row) for row in cursor.fetchall()]


class ScrapedDataRepository:
    @staticmethod
    def get_all(page=1, page_size=20, keyword="", source_id=None):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            query = "SELECT sd.*, ss.name as source_name FROM scraped_data sd LEFT JOIN scraping_sources ss ON sd.source_id = ss.id WHERE 1=1"
            params = []
            
            if keyword:
                query += " AND (sd.title LIKE ? OR sd.summary LIKE ?)"
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            
            if source_id:
                query += " AND sd.source_id = ?"
                params.append(source_id)
            
            query += " ORDER BY sd.id DESC LIMIT ? OFFSET ?"
            params.extend([page_size, offset])
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(keyword="", source_id=None):
        with get_connection() as conn:
            query = "SELECT COUNT(*) as count FROM scraped_data WHERE 1=1"
            params = []
            
            if keyword:
                query += " AND (title LIKE ? OR summary LIKE ?)"
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            
            if source_id:
                query += " AND source_id = ?"
                params.append(source_id)
            
            cursor = conn.execute(query, params)
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(data_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT sd.*, ss.name as source_name FROM scraped_data sd LEFT JOIN scraping_sources ss ON sd.source_id = ss.id WHERE sd.id = ?", (data_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create(source_id, title, url, summary='', content='', image_url=''):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO scraped_data (source_id, title, url, summary, content, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                (source_id, title, url, summary, content, image_url)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def batch_create(items):
        with get_connection() as conn:
            conn.executemany(
                "INSERT INTO scraped_data (source_id, title, url, summary, content, image_url) VALUES (?, ?, ?, ?, ?, ?)",
                items
            )
            conn.commit()
    
    @staticmethod
    def delete(data_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM scraped_data WHERE id = ?", (data_id,))
            conn.commit()
    
    @staticmethod
    def batch_delete(data_ids):
        with get_connection() as conn:
            placeholders = ','.join('?' * len(data_ids))
            conn.execute(f"DELETE FROM scraped_data WHERE id IN ({placeholders})", data_ids)
            conn.commit()
    
    @staticmethod
    def update_deep_scraped(data_id, deep_scraped=1):
        with get_connection() as conn:
            conn.execute("UPDATE scraped_data SET deep_scraped = ? WHERE id = ?", (deep_scraped, data_id))
            conn.commit()


class DeepScrapedDataRepository:
    @staticmethod
    def get_all(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            query = """
                SELECT dsd.*, sd.title as scraped_title, sd.url as scraped_url 
                FROM deep_scraped_data dsd 
                LEFT JOIN scraped_data sd ON dsd.scraped_data_id = sd.id 
                WHERE 1=1
            """
            params = []
            
            if keyword:
                query += " AND (dsd.title LIKE ? OR dsd.summary LIKE ? OR sd.title LIKE ?)"
                params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
            
            query += " ORDER BY dsd.id DESC LIMIT ? OFFSET ?"
            params.extend([page_size, offset])
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            query = """
                SELECT COUNT(*) as count 
                FROM deep_scraped_data dsd 
                LEFT JOIN scraped_data sd ON dsd.scraped_data_id = sd.id 
                WHERE 1=1
            """
            params = []
            
            if keyword:
                query += " AND (dsd.title LIKE ? OR dsd.summary LIKE ? OR sd.title LIKE ?)"
                params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])
            
            cursor = conn.execute(query, params)
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(data_id):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT dsd.*, sd.title as scraped_title, sd.url as scraped_url, ss.name as source_name 
                FROM deep_scraped_data dsd 
                LEFT JOIN scraped_data sd ON dsd.scraped_data_id = sd.id 
                LEFT JOIN scraping_sources ss ON sd.source_id = ss.id 
                WHERE dsd.id = ?
            """, (data_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_by_scraped_data_id(scraped_data_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM deep_scraped_data WHERE scraped_data_id = ?", (scraped_data_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create(scraped_data_id, title, url, raw_content='', structured_content='', 
               key_points='', entities='', sentiment='', summary='', full_text='', metadata=''):
        import json
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO deep_scraped_data 
                   (scraped_data_id, title, url, raw_content, structured_content, 
                    key_points, entities, sentiment, summary, full_text, metadata) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (scraped_data_id, title, url, 
                 json.dumps(raw_content) if isinstance(raw_content, (dict, list)) else raw_content,
                 json.dumps(structured_content) if isinstance(structured_content, (dict, list)) else structured_content,
                 json.dumps(key_points) if isinstance(key_points, (dict, list)) else key_points,
                 json.dumps(entities) if isinstance(entities, (dict, list)) else entities,
                 sentiment, summary, full_text,
                 json.dumps(metadata) if isinstance(metadata, (dict, list)) else metadata)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def delete(data_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM deep_scrape_logs WHERE scraped_data_id IN (SELECT scraped_data_id FROM deep_scraped_data WHERE id = ?)", (data_id,))
            conn.execute("DELETE FROM deep_scraped_data WHERE id = ?", (data_id,))
            conn.commit()
    
    @staticmethod
    def get_statistics():
        with get_connection() as conn:
            stats = {}
            
            cursor = conn.execute("SELECT COUNT(*) as total FROM deep_scraped_data")
            stats["total"] = cursor.fetchone()["total"]
            
            cursor = conn.execute("SELECT COUNT(*) as success FROM deep_scrape_logs WHERE status = 'success'")
            stats["success"] = cursor.fetchone()["success"]
            
            cursor = conn.execute("SELECT COUNT(*) as failed FROM deep_scrape_logs WHERE status = 'failed'")
            stats["failed"] = cursor.fetchone()["failed"]
            
            cursor = conn.execute("SELECT COALESCE(SUM(tokens_used), 0) as total_tokens FROM deep_scrape_logs")
            stats["total_tokens"] = cursor.fetchone()["total_tokens"]
            
            return stats


class DeepScrapeLogRepository:
    @staticmethod
    def get_all(page=1, page_size=20, scraped_data_id=None):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            query = "SELECT * FROM deep_scrape_logs WHERE 1=1"
            params = []
            
            if scraped_data_id:
                query += " AND scraped_data_id = ?"
                params.append(scraped_data_id)
            
            query += " ORDER BY id DESC LIMIT ? OFFSET ?"
            params.extend([page_size, offset])
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(scraped_data_id=None):
        with get_connection() as conn:
            query = "SELECT COUNT(*) as count FROM deep_scrape_logs WHERE 1=1"
            params = []
            
            if scraped_data_id:
                query += " AND scraped_data_id = ?"
                params.append(scraped_data_id)
            
            cursor = conn.execute(query, params)
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(log_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM deep_scrape_logs WHERE id = ?", (log_id,))
            return cursor.fetchone()
    
    @staticmethod
    def create(scraped_data_id, status, message='', start_time='', end_time='', 
               error_message='', tokens_used=0):
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO deep_scrape_logs 
                   (scraped_data_id, status, message, start_time, end_time, error_message, tokens_used) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (scraped_data_id, status, message, start_time, end_time, error_message, tokens_used)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update(log_id, status=None, message=None, end_time=None, error_message=None, tokens_used=None):
        with get_connection() as conn:
            updates = []
            params = []
            
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            if message is not None:
                updates.append("message = ?")
                params.append(message)
            if end_time is not None:
                updates.append("end_time = ?")
                params.append(end_time)
            if error_message is not None:
                updates.append("error_message = ?")
                params.append(error_message)
            if tokens_used is not None:
                updates.append("tokens_used = ?")
                params.append(tokens_used)
            
            if updates:
                params.append(log_id)
                conn.execute(f"UPDATE deep_scrape_logs SET {', '.join(updates)} WHERE id = ?", params)
                conn.commit()


class ConversationRepository:
    @staticmethod
    def get_all_by_user(user_id, page=1, page_size=20):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM conversations WHERE user_id = ? ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                (user_id, page_size, offset)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count_by_user(user_id):
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM conversations WHERE user_id = ?",
                (user_id,)
            )
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(conversation_id):
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (conversation_id,)
            )
            return cursor.fetchone()
    
    @staticmethod
    def create(user_id, title=None, model_engine_id=None):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO conversations (user_id, title, model_engine_id) VALUES (?, ?, ?)",
                (user_id, title, model_engine_id)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update(conversation_id, title=None, model_engine_id=None):
        with get_connection() as conn:
            updates = []
            params = []
            if title is not None:
                updates.append("title = ?")
                params.append(title)
            if model_engine_id is not None:
                updates.append("model_engine_id = ?")
                params.append(model_engine_id)
            
            if updates:
                updates.append("updated_at = datetime('now')")
                params.append(conversation_id)
                conn.execute(
                    f"UPDATE conversations SET {', '.join(updates)} WHERE id = ?",
                    params
                )
                conn.commit()
    
    @staticmethod
    def delete(conversation_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM conversation_messages WHERE conversation_id = ?", (conversation_id,))
            conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            conn.commit()


class ConversationMessageRepository:
    @staticmethod
    def get_by_conversation(conversation_id):
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM conversation_messages WHERE conversation_id = ? ORDER BY created_at ASC",
                (conversation_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def create(conversation_id, role, content):
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO conversation_messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def delete_by_conversation(conversation_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM conversation_messages WHERE conversation_id = ?", (conversation_id,))
            conn.commit()


class SkillRepository:
    @staticmethod
    def get_all(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT * FROM skills WHERE name LIKE ? OR skill_identifier LIKE ? ORDER BY sort_order ASC, id ASC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", f"%{keyword}%", page_size, offset)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM skills ORDER BY sort_order ASC, id ASC LIMIT ? OFFSET ?",
                    (page_size, offset)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def count(keyword=""):
        with get_connection() as conn:
            if keyword:
                cursor = conn.execute(
                    "SELECT COUNT(*) as count FROM skills WHERE name LIKE ? OR skill_identifier LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%")
                )
            else:
                cursor = conn.execute("SELECT COUNT(*) as count FROM skills")
            return cursor.fetchone()["count"]
    
    @staticmethod
    def get_by_id(skill_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM skills WHERE id = ?", (skill_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def get_by_identifier(skill_identifier):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM skills WHERE skill_identifier = ? AND enabled = 1", (skill_identifier,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create(skill_identifier, name, description="", skill_type="system", call_type="local", config=None, enabled=1, is_system=0, sort_order=0):
        import json
        config_str = json.dumps(config) if isinstance(config, (dict, list)) else config
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO skills (skill_identifier, name, description, skill_type, call_type, config, enabled, is_system, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (skill_identifier, name, description, skill_type, call_type, config_str, enabled, is_system, sort_order)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def update(skill_id, skill_identifier=None, name=None, description=None, skill_type=None, call_type=None, config=None, enabled=None, sort_order=None):
        import json
        with get_connection() as conn:
            updates = []
            params = []
            if skill_identifier is not None:
                updates.append("skill_identifier = ?")
                params.append(skill_identifier)
            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            if skill_type is not None:
                updates.append("skill_type = ?")
                params.append(skill_type)
            if call_type is not None:
                updates.append("call_type = ?")
                params.append(call_type)
            if config is not None:
                config_str = json.dumps(config) if isinstance(config, (dict, list)) else config
                updates.append("config = ?")
                params.append(config_str)
            if enabled is not None:
                updates.append("enabled = ?")
                params.append(enabled)
            if sort_order is not None:
                updates.append("sort_order = ?")
                params.append(sort_order)
            
            if updates:
                updates.append("updated_at = datetime('now')")
                params.append(skill_id)
                conn.execute(
                    f"UPDATE skills SET {', '.join(updates)} WHERE id = ?",
                    params
                )
                conn.commit()
    
    @staticmethod
    def delete(skill_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM role_skills WHERE skill_id = ?", (skill_id,))
            conn.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
            conn.commit()
    
    @staticmethod
    def get_enabled():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM skills WHERE enabled = 1 ORDER BY sort_order ASC, id ASC")
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_enabled_by_role(role_id):
        with get_connection() as conn:
            cursor = conn.execute(
                """SELECT s.* FROM skills s 
                   INNER JOIN role_skills rs ON s.id = rs.skill_id 
                   WHERE s.enabled = 1 AND rs.role_id = ? 
                   ORDER BY s.sort_order ASC, s.id ASC""",
                (role_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def set_role_skills(role_id, skill_ids):
        with get_connection() as conn:
            conn.execute("DELETE FROM role_skills WHERE role_id = ?", (role_id,))
            for skill_id in skill_ids:
                conn.execute(
                    "INSERT INTO role_skills (role_id, skill_id) VALUES (?, ?)",
                    (role_id, skill_id)
                )
            conn.commit()
    
    @staticmethod
    def get_role_skills(role_id):
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT skill_id FROM role_skills WHERE role_id = ?",
                (role_id,)
            )
            return [row["skill_id"] for row in cursor.fetchall()]
    
    @staticmethod
    def init_default_skills():
        """初始化内置技能"""
        default_skills = [
            {
                "skill_identifier": "search",
                "name": "网络搜索",
                "description": "调度全网搜索能力，获取关键词对应的实时网页资讯、公开信息。使用格式：/search 关键词",
                "skill_type": "system",
                "call_type": "api",
                "enabled": 1,
                "is_system": 1,
                "sort_order": 1
            },
            {
                "skill_identifier": "sql",
                "name": "数据问数",
                "description": "查询系统内采集数据、用户数据、运营统计等内部业务数据。使用格式：/sql 查询需求",
                "skill_type": "system",
                "call_type": "model_tool",
                "enabled": 1,
                "is_system": 1,
                "sort_order": 2
            },
            {
                "skill_identifier": "stat",
                "name": "数据统计",
                "description": "生成指定维度的统计分析结果，支持总量统计、趋势分析、占比统计等。使用格式：/stat 统计维度",
                "skill_type": "system",
                "call_type": "model_tool",
                "enabled": 1,
                "is_system": 1,
                "sort_order": 3
            },
            {
                "skill_identifier": "help",
                "name": "帮助指引",
                "description": "返回当前用户可用的全部技能列表，包含指令格式、功能说明与使用示例。",
                "skill_type": "system",
                "call_type": "local",
                "enabled": 1,
                "is_system": 1,
                "sort_order": 4
            },
            {
                "skill_identifier": "model",
                "name": "模型切换",
                "description": "对话过程中通过指令快速切换当前会话使用的大模型。使用格式：/model 模型名称",
                "skill_type": "system",
                "call_type": "local",
                "enabled": 1,
                "is_system": 1,
                "sort_order": 5
            }
        ]
        
        with get_connection() as conn:
            for skill in default_skills:
                cursor = conn.execute(
                    "SELECT id FROM skills WHERE skill_identifier = ?",
                    (skill["skill_identifier"],)
                )
                existing = cursor.fetchone()
                if not existing:
                    conn.execute(
                        """INSERT INTO skills (skill_identifier, name, description, skill_type, call_type, enabled, is_system, sort_order) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (skill["skill_identifier"], skill["name"], skill["description"], 
                         skill["skill_type"], skill["call_type"], skill["enabled"], 
                         skill["is_system"], skill["sort_order"])
                    )
            conn.commit()


class DigitalEmployeeRepository:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM digital_employees ORDER BY id ASC")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(employee_id):
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM digital_employees WHERE id = ?", (employee_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data):
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO digital_employees 
                (name, description, model_service, enable_switch_model, enable_play_music, enable_view_history, avatar)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.get("name"),
                    data.get("description", ""),
                    data.get("model_service", "默认模型"),
                    1 if data.get("enable_switch_model") else 0,
                    1 if data.get("enable_play_music") else 0,
                    1 if data.get("enable_view_history") else 0,
                    data.get("avatar", "")
                )
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update(employee_id, data):
        with get_connection() as conn:
            cursor = conn.execute(
                """
                UPDATE digital_employees 
                SET name = ?, description = ?, model_service = ?, 
                    enable_switch_model = ?, enable_play_music = ?, enable_view_history = ?,
                    avatar = ?, updated_at = datetime('now')
                WHERE id = ?
                """,
                (
                    data.get("name"),
                    data.get("description", ""),
                    data.get("model_service", "默认模型"),
                    1 if data.get("enable_switch_model") else 0,
                    1 if data.get("enable_play_music") else 0,
                    1 if data.get("enable_view_history") else 0,
                    data.get("avatar", ""),
                    employee_id
                )
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(employee_id):
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM digital_employees WHERE id = ?", (employee_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def init_default_data():
        default_employees = [
            {
                "name": "天气",
                "description": "根据用户的问题，调用模型引擎中的天气模型服务，获取天气信息。",
                "model_service": "默认模型",
                "enable_switch_model": 1,
                "enable_play_music": 0,
                "enable_view_history": 1,
                "avatar": "🌤️"
            },
            {
                "name": "音乐",
                "description": "根据用户的问题，调用模型引擎中的音乐模型服务，获取音乐信息。",
                "model_service": "默认模型",
                "enable_switch_model": 1,
                "enable_play_music": 1,
                "enable_view_history": 1,
                "avatar": "🎵"
            },
            {
                "name": "西师妹",
                "description": "根据用户的问题，调用模型引擎中的西师妹模型服务，获取对应关键词的信息。",
                "model_service": "默认模型",
                "enable_switch_model": 1,
                "enable_play_music": 0,
                "enable_view_history": 1,
                "avatar": "👩‍🎓"
            },
            {
                "name": "豆沙包ai",
                "description": "根据用户的问题，调用模型引擎中的豆沙包ai模型服务，获取对应关键词的信息。",
                "model_service": "默认模型",
                "enable_switch_model": 1,
                "enable_play_music": 0,
                "enable_view_history": 1,
                "avatar": "🥟"
            }
        ]
        
        with get_connection() as conn:
            for employee in default_employees:
                cursor = conn.execute("SELECT id FROM digital_employees WHERE name = ?", (employee["name"],))
                if not cursor.fetchone():
                    conn.execute(
                        """
                        INSERT INTO digital_employees 
                        (name, description, model_service, enable_switch_model, enable_play_music, enable_view_history, avatar)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            employee["name"],
                            employee["description"],
                            employee["model_service"],
                            employee["enable_switch_model"],
                            employee["enable_play_music"],
                            employee["enable_view_history"],
                            employee["avatar"]
                        )
                    )
            conn.commit()


class ReportRepository:
    @staticmethod
    def get_chat_statistics(start_date=None, end_date=None):
        with get_connection() as conn:
            stats = {}
            
            query_params = []
            date_cond = ""
            
            if start_date:
                date_cond += " AND DATE(c.created_at) >= ?"
                query_params.append(start_date)
            if end_date:
                date_cond += " AND DATE(c.created_at) <= ?"
                query_params.append(end_date)
            
            cursor = conn.execute(
                f"SELECT COUNT(*) as total FROM conversations c WHERE 1=1{date_cond}",
                query_params
            )
            stats["total_conversations"] = cursor.fetchone()["total"]
            
            cursor = conn.execute(
                f"SELECT COUNT(*) as total FROM conversation_messages cm JOIN conversations c ON cm.conversation_id = c.id WHERE 1=1{date_cond}",
                query_params
            )
            stats["total_messages"] = cursor.fetchone()["total"]
            
            cursor = conn.execute(
                f"SELECT COUNT(DISTINCT c.user_id) as total FROM conversations c WHERE 1=1{date_cond}",
                query_params
            )
            stats["active_users"] = cursor.fetchone()["total"]
            
            return stats

    @staticmethod
    def get_daily_statistics(days=7):
        with get_connection() as conn:
            cursor = conn.execute(f"""
                SELECT 
                    DATE(c.created_at) as date,
                    COUNT(DISTINCT c.id) as conversations,
                    COUNT(DISTINCT c.user_id) as users,
                    COUNT(cm.id) as messages
                FROM conversations c
                LEFT JOIN conversation_messages cm ON c.id = cm.conversation_id
                WHERE DATE(c.created_at) >= DATE('now', '-{days} days')
                GROUP BY DATE(c.created_at)
                ORDER BY date DESC
            """)
            result = []
            for row in cursor.fetchall():
                result.append({
                    "date": row["date"],
                    "conversations": row["conversations"],
                    "users": row["users"],
                    "messages": row["messages"]
                })
            return result

    @staticmethod
    def get_hourly_statistics():
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    strftime('%H', c.created_at) as hour,
                    COUNT(DISTINCT c.id) as conversations,
                    COUNT(cm.id) as messages
                FROM conversations c
                LEFT JOIN conversation_messages cm ON c.id = cm.conversation_id
                WHERE DATE(c.created_at) = DATE('now')
                GROUP BY strftime('%H', c.created_at)
                ORDER BY hour ASC
            """)
            result = []
            for row in cursor.fetchall():
                result.append({
                    "hour": row["hour"],
                    "conversations": row["conversations"],
                    "messages": row["messages"]
                })
            return result

    @staticmethod
    def get_top_questions(limit=10, start_date=None, end_date=None):
        with get_connection() as conn:
            query = """
                SELECT cm.content as question, 
                       COUNT(*) as frequency,
                       COUNT(DISTINCT c.user_id) as users
                FROM conversation_messages cm
                JOIN conversations c ON cm.conversation_id = c.id
                WHERE cm.role = 'user'
            """
            params = []
            
            if start_date:
                query += " AND DATE(c.created_at) >= ?"
                params.append(start_date)
            if end_date:
                query += " AND DATE(c.created_at) <= ?"
                params.append(end_date)
            
            query += " GROUP BY cm.content ORDER BY frequency DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            result = []
            for row in cursor.fetchall():
                result.append({
                    "question": row["question"],
                    "frequency": row["frequency"],
                    "users": row["users"]
                })
            return result

    @staticmethod
    def get_user_statistics(limit=10):
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT u.username,
                       COUNT(DISTINCT c.id) as conversations,
                       COUNT(cm.id) as messages,
                       MIN(c.created_at) as first_time,
                       MAX(c.created_at) as last_time
                FROM users u
                LEFT JOIN conversations c ON u.id = c.user_id
                LEFT JOIN conversation_messages cm ON c.id = cm.conversation_id
                GROUP BY u.id
                ORDER BY conversations DESC
                LIMIT ?
            """, (limit,))
            result = []
            for row in cursor.fetchall():
                result.append({
                    "username": row["username"],
                    "conversations": row["conversations"],
                    "messages": row["messages"],
                    "first_time": row["first_time"],
                    "last_time": row["last_time"]
                })
            return result

    @staticmethod
    def get_message_type_statistics(start_date=None, end_date=None):
        with get_connection() as conn:
            query = """
                SELECT cm.role, COUNT(*) as count
                FROM conversation_messages cm
                JOIN conversations c ON cm.conversation_id = c.id
                WHERE 1=1
            """
            params = []
            
            if start_date:
                query += " AND DATE(c.created_at) >= ?"
                params.append(start_date)
            if end_date:
                query += " AND DATE(c.created_at) <= ?"
                params.append(end_date)
            
            query += " GROUP BY cm.role"
            cursor = conn.execute(query, params)
            
            result = {"user": 0, "assistant": 0, "system": 0}
            for row in cursor.fetchall():
                result[row["role"]] = row["count"]
            
            return result

    @staticmethod
    def get_weekly_statistics(weeks=4):
        with get_connection() as conn:
            cursor = conn.execute(f"""
                SELECT 
                    strftime('%Y-%W', c.created_at) as week,
                    COUNT(DISTINCT c.id) as conversations,
                    COUNT(DISTINCT c.user_id) as users,
                    COUNT(cm.id) as messages
                FROM conversations c
                LEFT JOIN conversation_messages cm ON c.id = cm.conversation_id
                WHERE strftime('%Y-%W', c.created_at) >= strftime('%Y-%W', DATE('now', '-{weeks} weeks'))
                GROUP BY strftime('%Y-%W', c.created_at)
                ORDER BY week DESC
            """)
            result = []
            for row in cursor.fetchall():
                result.append({
                    "week": row["week"],
                    "conversations": row["conversations"],
                    "users": row["users"],
                    "messages": row["messages"]
                })
            return result

    @staticmethod
    def get_skill_usage_statistics(start_date=None, end_date=None):
        """按数字员工/技能分类统计使用次数"""
        with get_connection() as conn:
            query = """
                SELECT 
                    CASE
                        WHEN cm.content LIKE '@天气%' OR cm.content LIKE '%天气%' THEN '天气查询'
                        WHEN cm.content LIKE '@音乐%' OR cm.content LIKE '%音乐%' THEN '音乐检索'
                        WHEN cm.content LIKE '@西师妹%' OR cm.content LIKE '%西师妹%' THEN '西师妹对话'
                        WHEN cm.content LIKE '/search%' OR cm.content LIKE '%搜索%' THEN '联网搜索'
                        WHEN cm.content LIKE '%数据库%' OR cm.content LIKE '%查询%' OR cm.content LIKE '%统计%' THEN '数据查询'
                        ELSE '通用问题'
                    END as category,
                    COUNT(*) as count
                FROM conversation_messages cm
                JOIN conversations c ON cm.conversation_id = c.id
                WHERE cm.role = 'user'
            """
            params = []
            
            if start_date:
                query += " AND DATE(c.created_at) >= ?"
                params.append(start_date)
            if end_date:
                query += " AND DATE(c.created_at) <= ?"
                params.append(end_date)
            
            query += " GROUP BY category ORDER BY count DESC"
            cursor = conn.execute(query, params)
            
            result = []
            for row in cursor.fetchall():
                result.append({
                    "category": row["category"],
                    "count": row["count"]
                })
            return result

    @staticmethod
    def get_skill_usage_bar(start_date=None, end_date=None):
        """按数字员工名称统计使用次数（柱状图）"""
        with get_connection() as conn:
            query = """
                SELECT 
                    CASE
                        WHEN cm.content LIKE '@天气%' OR cm.content LIKE '%天气%' THEN '天气查询'
                        WHEN cm.content LIKE '@音乐%' OR cm.content LIKE '%音乐%' THEN '音乐检索'
                        WHEN cm.content LIKE '@西师妹%' OR cm.content LIKE '%西师妹%' THEN '西师妹对话'
                        WHEN cm.content LIKE '/search%' OR cm.content LIKE '%搜索%' THEN '联网搜索'
                        WHEN cm.content LIKE '%数据库%' OR cm.content LIKE '%查询%' OR cm.content LIKE '%统计%' THEN '数据查询'
                        ELSE '通用问题'
                    END as skill,
                    COUNT(*) as count
                FROM conversation_messages cm
                JOIN conversations c ON cm.conversation_id = c.id
                WHERE cm.role = 'user'
            """
            params = []
            
            if start_date:
                query += " AND DATE(c.created_at) >= ?"
                params.append(start_date)
            if end_date:
                query += " AND DATE(c.created_at) <= ?"
                params.append(end_date)
            
            query += " GROUP BY skill ORDER BY count DESC"
            cursor = conn.execute(query, params)
            
            result = []
            for row in cursor.fetchall():
                result.append({
                    "skill": row["skill"],
                    "count": row["count"]
                })
            return result


class SkillLogRepository:
    @staticmethod
    def create(user_id, skill_id, skill_name, input_content, output_content, status, error_message=None, duration_ms=0):
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO skill_logs (user_id, skill_id, skill_name, input_content, output_content, status, error_message, duration_ms) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, skill_id, skill_name, input_content, output_content, status, error_message, duration_ms)
            )
            conn.commit()
            return cursor.lastrowid

