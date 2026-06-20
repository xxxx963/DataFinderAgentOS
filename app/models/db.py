import  os
import sqlite3
from os.path import dirname

def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir))

DB_PATH=os.path.join(_project_root(), "database","app.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH) ,exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role_id INTEGER,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                is_default INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                icon TEXT,
                path TEXT,
                parent_id INTEGER DEFAULT 0,
                sort_order INTEGER DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS role_functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id INTEGER NOT NULL,
                function_id INTEGER NOT NULL
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS model_engines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                api_key TEXT NOT NULL,
                base_url TEXT NOT NULL,
                model_type TEXT NOT NULL DEFAULT 'text',
                temperature REAL DEFAULT 0.7,
                max_tokens INTEGER DEFAULT 2048,
                top_p REAL DEFAULT 1.0,
                system_prompt TEXT,
                is_default INTEGER NOT NULL DEFAULT 0,
                enable_sse INTEGER NOT NULL DEFAULT 0,
                enable_think INTEGER NOT NULL DEFAULT 0,
                token_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scraping_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                request_headers TEXT,
                method TEXT NOT NULL DEFAULT 'GET',
                enabled INTEGER NOT NULL DEFAULT 1,
                description TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                title TEXT,
                url TEXT NOT NULL,
                summary TEXT,
                content TEXT,
                image_url TEXT,
                scraped_at TEXT NOT NULL DEFAULT (datetime('now')),
                deep_scraped INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (source_id) REFERENCES scraping_sources(id)
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deep_scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scraped_data_id INTEGER NOT NULL,
                title TEXT,
                url TEXT NOT NULL,
                raw_content TEXT,
                structured_content TEXT,
                key_points TEXT,
                entities TEXT,
                sentiment TEXT,
                summary TEXT,
                full_text TEXT,
                metadata TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (scraped_data_id) REFERENCES scraped_data(id)
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deep_scrape_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scraped_data_id INTEGER,
                status TEXT NOT NULL,
                message TEXT,
                start_time TEXT,
                end_time TEXT,
                error_message TEXT,
                tokens_used INTEGER DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (scraped_data_id) REFERENCES scraped_data(id)
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT,
                model_engine_id INTEGER,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (model_engine_id) REFERENCES model_engines(id)
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_identifier TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                description TEXT,
                skill_type TEXT NOT NULL DEFAULT 'system',
                call_type TEXT NOT NULL DEFAULT 'local',
                config TEXT,
                enabled INTEGER NOT NULL DEFAULT 1,
                is_system INTEGER NOT NULL DEFAULT 0,
                sort_order INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        
        try:
            conn.execute("ALTER TABLE skills ADD COLUMN skill_identifier TEXT")
        except:
            pass
        try:
            conn.execute("ALTER TABLE skills ADD COLUMN call_type TEXT DEFAULT 'local'")
        except:
            pass
        try:
            conn.execute("ALTER TABLE skills ADD COLUMN is_system INTEGER DEFAULT 0")
        except:
            pass
        try:
            conn.execute("ALTER TABLE skills ADD COLUMN sort_order INTEGER DEFAULT 0")
        except:
            pass
        
        try:
            conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_skills_identifier ON skills(skill_identifier)")
        except:
            pass
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS role_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                FOREIGN KEY (role_id) REFERENCES roles(id),
                FOREIGN KEY (skill_id) REFERENCES skills(id),
                UNIQUE(role_id, skill_id)
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS skill_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                skill_name TEXT NOT NULL,
                input_content TEXT,
                output_content TEXT,
                status TEXT NOT NULL,
                error_message TEXT,
                duration_ms INTEGER DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (skill_id) REFERENCES skills(id)
            )
            """
        )
        
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS digital_employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                model_service TEXT NOT NULL DEFAULT '默认模型',
                enable_switch_model INTEGER NOT NULL DEFAULT 1,
                enable_play_music INTEGER NOT NULL DEFAULT 0,
                enable_view_history INTEGER NOT NULL DEFAULT 1,
                avatar TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


