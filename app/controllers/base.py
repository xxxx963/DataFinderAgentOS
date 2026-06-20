#整个控制层的基类，用于继承RequestHandler，对安全的配置做统一处理
from typing import Any

import  tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode('utf-8')
