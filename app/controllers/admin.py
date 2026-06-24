import tornado.web
from app.controllers.base import BaseHandler
from app.models.user import UserRepository
from app.models.system import RoleRepository, FunctionRepository, ModelEngineRepository, SkillRepository
import math
import json


class AdminLoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/admin")
            return
        self.render("admin/login.html", title="后台登录", error=None)

    def post(self):
        username = self.get_body_argument("username", "")
        password = self.get_body_argument("password", "")
        
        if not username or not password:
            self.set_status(400)
            return self.render("admin/login.html", title="后台登录", error="请输入用户名和密码")
        
        if not UserRepository.verify_user(username, password):
            self.set_status(401)
            return self.render("admin/login.html", title="后台登录", error="用户名或密码错误")
        
        self.set_secure_cookie("username", username)
        self.redirect("/admin")


class AdminLogoutHandler(BaseHandler):
    def post(self):
        self.clear_cookie("username")
        self.redirect("/admin/login")


class AdminHomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/layout.html", title="后台管理", username=self.current_user)


class VisualizationHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/placeholder.html", title="可视化", username=self.current_user)


class SmartScreenHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/placeholder.html", title="智能大屏", username=self.current_user)


class DigitalTwinHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/placeholder.html", title="数字孪生", username=self.current_user)


class NormalScreenHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/placeholder.html", title="普通大屏", username=self.current_user)


class RoleListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = self.get_argument("page", 1)
        try:
            page = int(page)
            if page < 1:
                page = 1
        except:
            page = 1
        
        keyword = self.get_argument("keyword", "")
        page_size = 20
        
        roles = RoleRepository.get_all(page, page_size, keyword)
        total = RoleRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        
        # 准备分页数据
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/roles.html", 
                    title="角色管理", 
                    username=self.current_user,
                    roles=roles,
                    page=page,
                    total_pages=total_pages,
                    keyword=keyword,
                    show_pagination=show_pagination,
                    has_prev=has_prev,
                    has_next=has_next,
                    prev_page=prev_page,
                    next_page=next_page,
                    page_numbers=page_numbers,
                    error=None)


class RoleEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, role_id=None):
        role = None
        all_functions = FunctionRepository.get_all_tree()
        selected_funcs = []
        
        if role_id and role_id != "new":
            role = RoleRepository.get_by_id(role_id)
            selected_funcs = RoleRepository.get_role_functions(role_id)
        
        self.render("admin/role_edit.html", 
                    title="角色管理", 
                    username=self.current_user,
                    role=role,
                    all_functions=all_functions,
                    selected_funcs=selected_funcs,
                    error=None)
    
    @tornado.web.authenticated
    def post(self, role_id=None):
        name = self.get_body_argument("name", "")
        description = self.get_body_argument("description", "")
        function_ids = self.get_body_arguments("function_ids")
        function_ids = [int(fid) for fid in function_ids if fid]
        
        if not name:
            self.set_status(400)
            all_functions = FunctionRepository.get_all_tree()
            return self.render("admin/role_edit.html", 
                              title="角色管理", 
                              username=self.current_user,
                              role={"id": role_id, "name": name, "description": description},
                              all_functions=all_functions,
                              selected_funcs=function_ids,
                              error="请输入角色名称")
        
        if role_id and role_id != "new":
            role = RoleRepository.get_by_id(role_id)
            if role and role.get("is_default") == 1:
                self.set_status(400)
                all_functions = FunctionRepository.get_all_tree()
                selected_funcs = RoleRepository.get_role_functions(role_id)
                return self.render("admin/role_edit.html", 
                                  title="角色管理", 
                                  username=self.current_user,
                                  role=role,
                                  all_functions=all_functions,
                                  selected_funcs=selected_funcs,
                                  error="默认角色不能修改")
            
            RoleRepository.update(role_id, name, description)
            RoleRepository.set_role_functions(role_id, function_ids)
        else:
            new_role_id = RoleRepository.create(name, description)
            RoleRepository.set_role_functions(new_role_id, function_ids)
        
        self.redirect("/admin/roles")


class RoleDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, role_id):
        role = RoleRepository.get_by_id(role_id)
        if role and role.get("is_default") == 1:
            self.set_status(400)
            page = self.get_argument("page", 1)
            keyword = self.get_argument("keyword", "")
            page_size = 20
            roles = RoleRepository.get_all(page, page_size, keyword)
            total = RoleRepository.count(keyword)
            total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
            
            # 准备分页数据
            show_pagination = total_pages > 1
            has_prev = page > 1
            has_next = page < total_pages
            prev_page = page - 1
            next_page = page + 1
            page_numbers = list(range(1, total_pages + 1))
            
            return self.render("admin/roles.html", 
                              title="角色管理", 
                              username=self.current_user,
                              roles=roles,
                              page=page,
                              total_pages=total_pages,
                              keyword=keyword,
                              show_pagination=show_pagination,
                              has_prev=has_prev,
                              has_next=has_next,
                              prev_page=prev_page,
                              next_page=next_page,
                              page_numbers=page_numbers,
                              error="默认角色不能删除")
        
        RoleRepository.delete(role_id)
        self.redirect("/admin/roles")


class UserListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = self.get_argument("page", 1)
        try:
            page = int(page)
            if page < 1:
                page = 1
        except:
            page = 1
        
        keyword = self.get_argument("keyword", "")
        page_size = 20
        
        users = UserRepository.get_all(page, page_size, keyword)
        total = UserRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        roles = RoleRepository.get_all(1, 1000)
        
        # 准备分页数据
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/users.html", 
                    title="用户管理", 
                    username=self.current_user,
                    users=users,
                    roles=roles,
                    page=page,
                    total_pages=total_pages,
                    keyword=keyword,
                    show_pagination=show_pagination,
                    has_prev=has_prev,
                    has_next=has_next,
                    prev_page=prev_page,
                    next_page=next_page,
                    page_numbers=page_numbers,
                    error=None)


class UserEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id=None):
        user = None
        roles = RoleRepository.get_all(1, 1000)
        
        if user_id and user_id != "new":
            user = UserRepository.get_by_id(user_id)
        
        self.render("admin/user_edit.html", 
                    title="用户管理", 
                    username=self.current_user,
                    user=user,
                    roles=roles,
                    error=None)
    
    @tornado.web.authenticated
    def post(self, user_id=None):
        username = self.get_body_argument("username", "")
        password = self.get_body_argument("password", "")
        role_id = self.get_body_argument("role_id", None)
        if role_id:
            role_id = int(role_id)
        
        if not username:
            self.set_status(400)
            roles = RoleRepository.get_all(1, 1000)
            return self.render("admin/user_edit.html", 
                              title="用户管理", 
                              username=self.current_user,
                              user={"id": user_id, "username": username, "role_id": role_id},
                              roles=roles,
                              error="请输入用户名")
        
        if user_id and user_id != "new":
            user = UserRepository.get_by_id(user_id)
            if user and user.get("username") == "admin":
                roles = RoleRepository.get_all(1, 1000)
                return self.render("admin/user_edit.html", 
                                  title="用户管理", 
                                  username=self.current_user,
                                  user=user,
                                  roles=roles,
                                  error="admin用户不能修改")
            
            UserRepository.update_user(user_id, username, role_id)
            if password:
                UserRepository.update_password(user_id, password)
        else:
            if not password:
                self.set_status(400)
                roles = RoleRepository.get_all(1, 1000)
                return self.render("admin/user_edit.html", 
                                  title="用户管理", 
                                  username=self.current_user,
                                  user={"username": username, "role_id": role_id},
                                  roles=roles,
                                  error="请输入密码")
            UserRepository.create_user(username, password, role_id)
        
        self.redirect("/admin/users")


class UserDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, user_id):
        user = UserRepository.get_by_id(user_id)
        if user and user.get("username") == "admin":
            page = self.get_argument("page", 1)
            keyword = self.get_argument("keyword", "")
            page_size = 20
            users = UserRepository.get_all(page, page_size, keyword)
            total = UserRepository.count(keyword)
            total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
            roles = RoleRepository.get_all(1, 1000)
            
            # 准备分页数据
            show_pagination = total_pages > 1
            has_prev = page > 1
            has_next = page < total_pages
            prev_page = page - 1
            next_page = page + 1
            page_numbers = list(range(1, total_pages + 1))
            
            return self.render("admin/users.html", 
                              title="用户管理", 
                              username=self.current_user,
                              users=users,
                              roles=roles,
                              page=page,
                              total_pages=total_pages,
                              keyword=keyword,
                              show_pagination=show_pagination,
                              has_prev=has_prev,
                              has_next=has_next,
                              prev_page=prev_page,
                              next_page=next_page,
                              page_numbers=page_numbers,
                              error="admin用户不能删除")
        
        UserRepository.delete_user(user_id)
        self.redirect("/admin/users")


class FunctionListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = self.get_argument("page", 1)
        try:
            page = int(page)
            if page < 1:
                page = 1
        except:
            page = 1
        
        keyword = self.get_argument("keyword", "")
        page_size = 20
        
        functions = FunctionRepository.get_all(page, page_size, keyword)
        total = FunctionRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        all_functions = FunctionRepository.get_all_tree()
        
        # 准备分页数据
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/functions.html", 
                    title="功能管理", 
                    username=self.current_user,
                    functions=functions,
                    all_functions=all_functions,
                    page=page,
                    total_pages=total_pages,
                    keyword=keyword,
                    show_pagination=show_pagination,
                    has_prev=has_prev,
                    has_next=has_next,
                    prev_page=prev_page,
                    next_page=next_page,
                    page_numbers=page_numbers,
                    error=None)


class FunctionEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, func_id=None):
        func = None
        all_functions = FunctionRepository.get_all_tree()
        
        if func_id and func_id != "new":
            func = FunctionRepository.get_by_id(func_id)
        
        self.render("admin/function_edit.html", 
                    title="功能管理", 
                    username=self.current_user,
                    func=func,
                    all_functions=all_functions,
                    error=None)
    
    @tornado.web.authenticated
    def post(self, func_id=None):
        name = self.get_body_argument("name", "")
        icon = self.get_body_argument("icon", "")
        path = self.get_body_argument("path", "")
        parent_id = self.get_body_argument("parent_id", 0)
        sort_order = self.get_body_argument("sort_order", 0)
        
        try:
            parent_id = int(parent_id)
            sort_order = int(sort_order)
        except:
            parent_id = 0
            sort_order = 0
        
        if not name:
            self.set_status(400)
            all_functions = FunctionRepository.get_all_tree()
            return self.render("admin/function_edit.html", 
                              title="功能管理", 
                              username=self.current_user,
                              func={"id": func_id, "name": name, "icon": icon, "path": path, "parent_id": parent_id, "sort_order": sort_order},
                              all_functions=all_functions,
                              error="请输入功能名称")
        
        if func_id and func_id != "new":
            FunctionRepository.update(func_id, name, icon, path, parent_id, sort_order)
        else:
            FunctionRepository.create(name, icon, path, parent_id, sort_order)
        
        self.redirect("/admin/functions")


class FunctionDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, func_id):
        FunctionRepository.delete(func_id)
        self.redirect("/admin/functions")


class ModelEngineListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = self.get_argument("page", 1)
        try:
            page = int(page)
            if page < 1:
                page = 1
        except:
            page = 1
        
        keyword = self.get_argument("keyword", "")
        page_size = 6
        
        model_engines = ModelEngineRepository.get_all(page, page_size, keyword)
        total = ModelEngineRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/model_engines.html", 
                    title="模型引擎", 
                    username=self.current_user,
                    model_engines=model_engines,
                    page=page,
                    total_pages=total_pages,
                    keyword=keyword,
                    show_pagination=show_pagination,
                    has_prev=has_prev,
                    has_next=has_next,
                    prev_page=prev_page,
                    next_page=next_page,
                    page_numbers=page_numbers,
                    error=None)


class ModelEngineEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, model_id=None):
        model_engine = None
        
        if model_id and model_id != "new":
            model_engine = ModelEngineRepository.get_by_id(model_id)
        
        self.render("admin/model_engine_edit.html", 
                    title="模型引擎", 
                    username=self.current_user,
                    model_engine=model_engine,
                    error=None)
    
    @tornado.web.authenticated
    def post(self, model_id=None):
        name = self.get_body_argument("name", "")
        model_name = self.get_body_argument("model_name", "")
        api_key = self.get_body_argument("api_key", "")
        base_url = self.get_body_argument("base_url", "")
        model_type = self.get_body_argument("model_type", "text")
        temperature = self.get_body_argument("temperature", "0.7")
        max_tokens = self.get_body_argument("max_tokens", "2048")
        top_p = self.get_body_argument("top_p", "1.0")
        system_prompt = self.get_body_argument("system_prompt", "")
        is_default = self.get_body_argument("is_default", "0")
        enable_sse = self.get_body_argument("enable_sse", "0")
        enable_think = self.get_body_argument("enable_think", "0")
        
        try:
            temperature = float(temperature)
            max_tokens = int(max_tokens)
            top_p = float(top_p)
            is_default = int(is_default)
            enable_sse = int(enable_sse)
            enable_think = int(enable_think)
        except:
            temperature = 0.7
            max_tokens = 2048
            top_p = 1.0
            is_default = 0
            enable_sse = 0
            enable_think = 0
        
        if not name or not model_name or not api_key or not base_url:
            self.set_status(400)
            return self.render("admin/model_engine_edit.html", 
                              title="模型引擎", 
                              username=self.current_user,
                              model_engine={"id": model_id, "name": name, "model_name": model_name, 
                                          "api_key": api_key, "base_url": base_url, 
                                          "model_type": model_type, "temperature": temperature, 
                                          "max_tokens": max_tokens, "top_p": top_p, 
                                          "system_prompt": system_prompt, "is_default": is_default, 
                                          "enable_sse": enable_sse, "enable_think": enable_think},
                              error="请填写所有必填字段")
        
        if model_id and model_id != "new":
            ModelEngineRepository.update(model_id, name, model_name, api_key, base_url, 
                                        model_type, temperature, max_tokens, top_p, 
                                        system_prompt, is_default, enable_sse, enable_think)
        else:
            ModelEngineRepository.create(name, model_name, api_key, base_url, model_type, 
                                        temperature, max_tokens, top_p, system_prompt, 
                                        is_default, enable_sse, enable_think)
        
        self.redirect("/admin/model-engines")


class ModelEngineDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, model_id):
        ModelEngineRepository.delete(model_id)
        self.redirect("/admin/model-engines")


class ModelEngineSetDefaultHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, model_id):
        ModelEngineRepository.set_default(model_id)
        self.redirect("/admin/model-engines")


class ModelEngineChatHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, model_id):
        model_engine = ModelEngineRepository.get_by_id(model_id)
        if not model_engine:
            self.set_status(404)
            return
        
        self.render("admin/model_engine_chat.html", 
                    title="模型测试", 
                    username=self.current_user,
                    model_engine=model_engine)
    
    @tornado.web.authenticated
    def post(self, model_id):
        model_engine = ModelEngineRepository.get_by_id(model_id)
        if not model_engine:
            self.set_status(404)
            self.write({"success": False, "error": "模型不存在"})
            return
        
        user_message = self.get_body_argument("message", "")
        if not user_message:
            self.write({"success": False, "error": "请输入消息"})
            return
        
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=model_engine["api_key"],
                base_url=model_engine["base_url"]
            )
            
            messages = []
            if model_engine["system_prompt"]:
                messages.append({"role": "system", "content": model_engine["system_prompt"]})
            messages.append({"role": "user", "content": user_message})
            
            response = client.chat.completions.create(
                model=model_engine["model_name"],
                messages=messages,
                temperature=model_engine["temperature"],
                max_tokens=model_engine["max_tokens"],
                top_p=model_engine["top_p"],
                stream=bool(model_engine["enable_sse"])
            )
            
            if model_engine["enable_sse"]:
                self.set_header("Content-Type", "text/event-stream")
                self.set_header("Cache-Control", "no-cache")
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        self.write(f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n")
                        self.flush()
                self.write(f"data: {json.dumps({'done': True})}\n\n")
                self.flush()
            else:
                assistant_message = response.choices[0].message.content
                
                total_tokens = response.usage.total_tokens if hasattr(response, 'usage') else 0
                if total_tokens > 0:
                    ModelEngineRepository.update_token_count(model_id, total_tokens)
                
                self.write({"success": True, "content": assistant_message, "tokens": total_tokens})
        except Exception as e:
            self.write({"success": False, "error": str(e)})


class SkillListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # 初始化内置技能
        SkillRepository.init_default_skills()
        
        page = self.get_argument("page", 1)
        try:
            page = int(page)
            if page < 1:
                page = 1
        except:
            page = 1
        
        keyword = self.get_argument("keyword", "")
        page_size = 20
        
        skills = SkillRepository.get_all(page, page_size, keyword)
        total = SkillRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/skills.html", 
                    title="技能仓库", 
                    username=self.current_user,
                    skills=skills,
                    page=page,
                    total_pages=total_pages,
                    keyword=keyword,
                    show_pagination=show_pagination,
                    has_prev=has_prev,
                    has_next=has_next,
                    prev_page=prev_page,
                    next_page=next_page,
                    page_numbers=page_numbers,
                    error=None)


class SkillEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, skill_id=None):
        skill = None
        
        if skill_id and skill_id != "new":
            skill = SkillRepository.get_by_id(skill_id)
        
        self.render("admin/skill_edit.html", 
                    title="技能管理", 
                    username=self.current_user,
                    skill=skill,
                    error=None)
    
    @tornado.web.authenticated
    def post(self, skill_id=None):
        skill_identifier = self.get_body_argument("skill_identifier", "").strip()
        name = self.get_body_argument("name", "").strip()
        description = self.get_body_argument("description", "")
        skill_type = self.get_body_argument("skill_type", "system")
        call_type = self.get_body_argument("call_type", "local")
        enabled = self.get_body_argument("enabled", "1")
        sort_order = self.get_body_argument("sort_order", "0")
        
        try:
            enabled = int(enabled)
            sort_order = int(sort_order)
        except:
            enabled = 1
            sort_order = 0
        
        if not skill_identifier or not name:
            self.set_status(400)
            return self.render("admin/skill_edit.html", 
                              title="技能管理", 
                              username=self.current_user,
                              skill={"id": skill_id, "skill_identifier": skill_identifier, "name": name, 
                                    "description": description, "skill_type": skill_type, 
                                    "call_type": call_type, "enabled": enabled, "sort_order": sort_order},
                              error="请填写技能标识和技能名称")
        
        if skill_id and skill_id != "new":
            skill = SkillRepository.get_by_id(skill_id)
            if skill and skill.get("is_system") == 1:
                # 系统内置技能只允许修改描述、启用状态和排序
                SkillRepository.update(skill_id, 
                                      name=name, 
                                      description=description, 
                                      enabled=enabled, 
                                      sort_order=sort_order)
            else:
                SkillRepository.update(skill_id, 
                                      skill_identifier=skill_identifier, 
                                      name=name, 
                                      description=description, 
                                      skill_type=skill_type, 
                                      call_type=call_type, 
                                      enabled=enabled, 
                                      sort_order=sort_order)
        else:
            SkillRepository.create(skill_identifier, name, description, skill_type, call_type, 
                                  config=None, enabled=enabled, is_system=0, sort_order=sort_order)
        
        self.redirect("/admin/skills")


class SkillDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, skill_id):
        skill = SkillRepository.get_by_id(skill_id)
        if skill and skill.get("is_system") == 1:
            self.set_status(400)
            page = self.get_argument("page", 1)
            keyword = self.get_argument("keyword", "")
            page_size = 20
            skills = SkillRepository.get_all(page, page_size, keyword)
            total = SkillRepository.count(keyword)
            total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
            
            show_pagination = total_pages > 1
            has_prev = page > 1
            has_next = page < total_pages
            prev_page = page - 1
            next_page = page + 1
            page_numbers = list(range(1, total_pages + 1))
            
            return self.render("admin/skills.html", 
                              title="技能仓库", 
                              username=self.current_user,
                              skills=skills,
                              page=page,
                              total_pages=total_pages,
                              keyword=keyword,
                              show_pagination=show_pagination,
                              has_prev=has_prev,
                              has_next=has_next,
                              prev_page=prev_page,
                              next_page=next_page,
                              page_numbers=page_numbers,
                              error="系统内置技能不能删除")
        
        SkillRepository.delete(skill_id)
        self.redirect("/admin/skills")
