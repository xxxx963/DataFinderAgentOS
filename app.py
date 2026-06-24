#主入口程序，主要是加载程序、加载和管理路由、配置访问控制以及服务器启动配置等
import os
import secrets

#v0.1版本 ：用于验证tornado框架的最小示例，主要是验证路由、程序加载、服务器启动
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer

from app.controllers.base import BaseHandler

from app.controllers.auth import LogoutHandler, LoginHandler, RegisterHandler
from app.controllers.home import HomeHandler
from app.controllers.chat import ChatHandler, ModelsHandler, ConversationsHandler, ConversationDetailHandler, ChatStreamHandler, DigitalEmployeesHandler, SkillsApiHandler
from app.controllers.admin import (
    AdminLoginHandler, AdminLogoutHandler, AdminHomeHandler,
    VisualizationHandler, SmartScreenHandler, DigitalTwinHandler, NormalScreenHandler,
    RoleListHandler, RoleEditHandler, RoleDeleteHandler,
    UserListHandler, UserEditHandler, UserDeleteHandler,
    FunctionListHandler, FunctionEditHandler, FunctionDeleteHandler,
    ModelEngineListHandler, ModelEngineEditHandler, ModelEngineDeleteHandler,
    ModelEngineSetDefaultHandler, ModelEngineChatHandler,
    SkillListHandler, SkillEditHandler, SkillDeleteHandler
)
from app.controllers.watchtower import (
    WatchtowerSourceListHandler, WatchtowerSourceEditHandler, WatchtowerSourceDeleteHandler
)
from app.controllers.scraping import (
    ScrapingSourceListHandler, ScrapingSourceEditHandler, ScrapingSourceDeleteHandler,
    ScrapingHandler, ScrapingSaveHandler, ScrapedDataListHandler,
    ScrapedDataDeleteHandler, ScrapedDataDeleteMultipleHandler, WatchtowerHandler,
    DeepScrapeHandler, DeepScrapeExecuteHandler, DeepScrapeDetailHandler,
    DeepScrapeDeleteHandler
)
from app.controllers.report import ReportHandler, ReportApiHandler, ReportExportHandler
from app.controllers.digital_employee import DigitalEmployeeHandler, DigitalEmployeeApiHandler
from app.models.db import init_db

 #web应用
def app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    settings = dict(
        template_path=os.path.join(basedir, "app", "templates"),
        static_path=os.path.join(basedir, "app", "static"),
        cookie_secret=os.environ.get("COOKIE_SECRET", secrets.token_hex(32)),
        login_url="/admin/login",
        xsrf_cookies=False,
        debug=True,
        autoreload=True

    )


    return tornado.web.Application([
        ("/", LoginHandler),
        ("/register", RegisterHandler),
        ("/home", ChatHandler),
        ("/user/login", LoginHandler),
        ("/user/logout", LogoutHandler),
        ("/logout", LogoutHandler),
        ("/api/models", ModelsHandler),
        ("/api/skills", SkillsApiHandler),
        ("/api/employees", DigitalEmployeesHandler),
        ("/api/conversations", ConversationsHandler),
        ("/api/conversations/(.*)", ConversationDetailHandler),
        ("/api/chat/stream", ChatStreamHandler),
        ("/admin/login", AdminLoginHandler),
        ("/admin/logout", AdminLogoutHandler),
        ("/admin", AdminHomeHandler),
        ("/admin/visualization", VisualizationHandler),
        ("/admin/smart-screen", SmartScreenHandler),
        ("/admin/digital-twin", DigitalTwinHandler),
        ("/admin/normal-screen", NormalScreenHandler),
        ("/admin/roles", RoleListHandler),
        ("/admin/roles/(.*)", RoleEditHandler),
        ("/admin/roles/delete/(.*)", RoleDeleteHandler),
        ("/admin/users", UserListHandler),
        ("/admin/users/(.*)", UserEditHandler),
        ("/admin/users/delete/(.*)", UserDeleteHandler),
        ("/admin/functions", FunctionListHandler),
        ("/admin/functions/(.*)", FunctionEditHandler),
        ("/admin/functions/delete/(.*)", FunctionDeleteHandler),
        ("/admin/model-engines", ModelEngineListHandler),
        ("/admin/model-engines/new", ModelEngineEditHandler),
        ("/admin/model-engines/delete/(.*)", ModelEngineDeleteHandler),
        ("/admin/model-engines/set-default/(.*)", ModelEngineSetDefaultHandler),
        ("/admin/model-engines/chat/(.*)", ModelEngineChatHandler),
        ("/admin/model-engines/(.*)", ModelEngineEditHandler),
        ("/admin/watchtower-sources", WatchtowerSourceListHandler),
        ("/admin/watchtower-sources/new", WatchtowerSourceEditHandler),
        ("/admin/watchtower-sources/delete/(.*)", WatchtowerSourceDeleteHandler),
        ("/admin/watchtower-sources/(.*)", WatchtowerSourceEditHandler),
        ("/admin/scraping-sources", ScrapingSourceListHandler),
        ("/admin/scraping-sources/new", ScrapingSourceEditHandler),
        ("/admin/scraping-sources/delete/(.*)", ScrapingSourceDeleteHandler),
        ("/admin/scraping-sources/(.*)", ScrapingSourceEditHandler),
        ("/admin/watchtower", WatchtowerHandler),
        ("/admin/scraping", ScrapingHandler),
        ("/admin/scraping/search", ScrapingHandler),
        ("/admin/scraping/save", ScrapingSaveHandler),
        ("/admin/scraped-data", ScrapedDataListHandler),
        ("/admin/scraped-data/delete/(.*)", ScrapedDataDeleteHandler),
        ("/admin/scraped-data/delete-multiple", ScrapedDataDeleteMultipleHandler),
        ("/admin/deep-scrape", DeepScrapeHandler),
        ("/admin/deep-scrape/execute", DeepScrapeExecuteHandler),
        ("/admin/deep-scrape/(.*)", DeepScrapeDetailHandler),
        ("/admin/deep-scrape/delete/(.*)", DeepScrapeDeleteHandler),
        ("/admin/skills", SkillListHandler),
        ("/admin/skills/new", SkillEditHandler),
        ("/admin/skills/delete/(.*)", SkillDeleteHandler),
        ("/admin/skills/(.*)", SkillEditHandler),
        ("/admin/report", ReportHandler),
        ("/admin/report/api", ReportApiHandler),
        ("/admin/report/export", ReportExportHandler),
        ("/admin/digital-employee", DigitalEmployeeHandler),
        ("/admin/digital-employee/api", DigitalEmployeeApiHandler),
        ("/admin/digital-employee/api/(.*)", DigitalEmployeeApiHandler)
    ],
        **settings
    )


if __name__ == "__main__":
    init_db()
    app=app()
    server=HTTPServer(app)
    server.listen(10086)
    print("Server Started:http://localhost:10086/",flush=True)
    tornado.ioloop.IOLoop.current().start()


