# 初始化数据库，创建默认用户
from app.models.user import UserRepository
from app.models.db import init_db
from app.models.db import get_connection

def init_default_data():
    import json
    with get_connection() as conn:
        # 创建默认角色
        cursor = conn.execute("SELECT id FROM roles WHERE name = ?", ("超级管理员",))
        if not cursor.fetchone():
            cursor = conn.execute(
                "INSERT INTO roles (name, description, is_default) VALUES (?, ?, ?)",
                ("超级管理员", "系统超级管理员，拥有所有权限", 1)
            )
            admin_role_id = cursor.lastrowid
            
            cursor = conn.execute(
                "INSERT INTO roles (name, description, is_default) VALUES (?, ?, ?)",
                ("普通用户", "普通用户角色，只有前台权限", 0)
            )
            user_role_id = cursor.lastrowid
        else:
            cursor = conn.execute("SELECT id FROM roles WHERE name = ?", ("超级管理员",))
            admin_role_id = cursor.fetchone()["id"]
        
        # 创建默认功能
        default_functions = [
            ("系统管理", "fas fa-users-cog", "", 0, 1),
            ("用户管理", "fas fa-user", "/admin/users", 1, 1),
            ("角色管理", "fas fa-user-tag", "/admin/roles", 1, 2),
            ("功能管理", "fas fa-th-list", "/admin/functions", 1, 3),
            ("智能引擎", "fas fa-brain", "", 0, 2),
            ("模型引擎", "fas fa-cogs", "/admin/model-engines", 5, 1),
            ("技能仓库", "fas fa-toolbox", "", 5, 2),
            ("数字员工", "fas fa-robot", "", 5, 3),
            ("瞭望管理", "fas fa-binoculars", "", 0, 3),
            ("采集源管理", "fas fa-cog", "/admin/scraping-sources", 9, 1),
            ("瞭望采集", "fas fa-search", "/admin/scraping", 9, 2),
            ("数据仓库", "fas fa-warehouse", "/admin/scraped-data", 9, 3),
            ("深度采集", "fas fa-search-plus", "", 9, 4),
            ("可视化", "fas fa-tv", "", 0, 4),
            ("智能大屏", "fas fa-chart-area", "", 13, 1),
            ("数字孪生", "fas fa-cube", "", 13, 2),
            ("普通大屏", "fas fa-desktop", "", 13, 3),
        ]
        
        func_ids = []
        for name, icon, path, parent_id, sort_order in default_functions:
            cursor = conn.execute(
                "SELECT id FROM functions WHERE name = ?",
                (name,)
            )
            existing = cursor.fetchone()
            if not existing:
                cursor = conn.execute(
                    "INSERT INTO functions (name, icon, path, parent_id, sort_order) VALUES (?, ?, ?, ?, ?)",
                    (name, icon, path, parent_id, sort_order)
                )
                func_ids.append(cursor.lastrowid)
            else:
                func_ids.append(existing["id"])
        
        # 为超级管理员分配所有功能
        conn.execute("DELETE FROM role_functions WHERE role_id = ?", (admin_role_id,))
        for func_id in func_ids:
            conn.execute(
                "INSERT INTO role_functions (role_id, function_id) VALUES (?, ?)",
                (admin_role_id, func_id)
            )
        
        # 创建或更新admin用户
        import hashlib
        import secrets
        
        def _hash_password(password, salt):
            dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
            return dk.hex()
        
        cursor = conn.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        admin_user = cursor.fetchone()
        if not admin_user:
            salt_bytes = secrets.token_bytes(16)
            password_hash = _hash_password("admin888", salt_bytes)
            salt_hex = salt_bytes.hex()
            conn.execute(
                "INSERT INTO users (username, password_hash, salt, role_id) VALUES (?, ?, ?, ?)",
                ("admin", password_hash, salt_hex, admin_role_id)
            )
        else:
            conn.execute(
                "UPDATE users SET role_id = ? WHERE username = ?",
                (admin_role_id, "admin")
            )
        
        # 创建默认采集源（百度新闻）
        baidu_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.baidu.com",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0"
        }
        
        cursor = conn.execute("SELECT id FROM scraping_sources WHERE name = ?", ("百度新闻",))
        if not cursor.fetchone():
            conn.execute(
                "INSERT INTO scraping_sources (name, url, request_headers, method, enabled, description) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "百度新闻", 
                    "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word={keyword}&pn=0", 
                    json.dumps(baidu_headers), 
                    "GET", 
                    1, 
                    "百度新闻搜索采集源"
                )
            )
        
        conn.commit()

def main():
    print("初始化数据库...")
    init_db()
    
    print("初始化默认数据...")
    init_default_data()
    
    print("初始化完成！")
    print("默认账号: admin")
    print("默认密码: admin888")

if __name__ == "__main__":
    main()
