from calendar import error

import  tornado.web
from app.controllers.base import BaseHandler
from app.models.user import UserRepository
from app.models.db import get_connection


class LoginHandler(BaseHandler):
    def get(self):
        self.render("web\\login.html",title="登录",error=None)

    def post(self):
        username = self.get_body_argument("username","")
        password = self.get_body_argument("password","")
        if not username or not password:
            self.set_status(400)
            return self.render("web\\login.html",title="登录",error="请输入用户名和密码")

        if not UserRepository.verify_user(username,password):
            self.set_status(401)
            return self.render("web\\login.html",title="登录",error="用户和密码错误")
        
        # 获取用户角色信息
        user = UserRepository.get_user_by_username(username)
        
        # 设置安全cookie
        self.set_secure_cookie("username", username)
        self.set_secure_cookie("user_id", str(user["id"]) if user else "")
        self.set_secure_cookie("role_id", str(user["role_id"]) if user else "")
        
        # 检查是否是管理员角色
        with get_connection() as conn:
            cursor = conn.execute("SELECT name FROM roles WHERE id = ?", (user["role_id"],))
            role = cursor.fetchone()
            if role and role["name"] == "超级管理员":
                self.redirect("/admin")
            else:
                self.redirect("/home")


class RegisterHandler(BaseHandler):
    def get(self):
        self.render("web\\register.html", title="注册", error=None)
    
    def post(self):
        username = self.get_body_argument("username", "")
        password = self.get_body_argument("password", "")
        confirm_password = self.get_body_argument("confirm_password", "")
        
        # 验证输入
        if not username or not password:
            return self.render("web\\register.html", title="注册", error="请输入用户名和密码")
        
        if password != confirm_password:
            return self.render("web\\register.html", title="注册", error="两次输入的密码不一致")
        
        if len(password) < 6:
            return self.render("web\\register.html", title="注册", error="密码至少需要6个字符")
        
        # 获取普通用户角色ID
        role_id = None
        with get_connection() as conn:
            cursor = conn.execute("SELECT id FROM roles WHERE name = ?", ("普通用户",))
            role = cursor.fetchone()
            if role:
                role_id = role["id"]
        
        # 创建用户
        if not UserRepository.create_user(username, password, role_id=role_id):
            return self.render("web\\register.html", title="注册", error="用户名已存在")
        
        # 注册成功，跳转到登录页
        self.redirect("/")


class LogoutHandler(BaseHandler):
    def post(self):
        self.clear_cookie('username')
        self.clear_cookie('user_id')
        self.clear_cookie('role_id')
        self.redirect("/")