import tornado.web
from app.controllers.base import BaseHandler
from app.models.watchtower import WatchtowerSourceRepository
import math
import json

class WatchtowerSourceListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = self.get_argument("page", 1)
        try:
            page = int(page)
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        
        keyword = self.get_argument("keyword", "")
        page_size = 20
        
        sources = WatchtowerSourceRepository.get_all(page, page_size, keyword)
        total = WatchtowerSourceRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        
        # Prepare pagination data
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/watchtower_sources.html", 
                    title="瞭望源管理", 
                    username=self.current_user,
                    sources=sources,
                    page=page,
                    total_pages=total_pages,
                    total=total,
                    keyword=keyword,
                    show_pagination=show_pagination,
                    has_prev=has_prev,
                    has_next=has_next,
                    prev_page=prev_page,
                    next_page=next_page,
                    page_numbers=page_numbers,
                    error=None)


class WatchtowerSourceEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, source_id=None):
        source = None
        if source_id and source_id != "new":
            source = WatchtowerSourceRepository.get_by_id(source_id)
        
        self.render("admin/watchtower_source_edit.html", 
                    title="瞭望源管理", 
                    username=self.current_user,
                    source=source,
                    error=None)
    
    @tornado.web.authenticated
    def post(self, source_id=None):
        name = self.get_body_argument("name", "")
        url = self.get_body_argument("url", "")
        request_headers = self.get_body_argument("request_headers", "")
        method = self.get_body_argument("method", "GET")
        enabled = 1 if self.get_body_argument("enabled", "0") == "1" else 0
        description = self.get_body_argument("description", "")
        
        if not name or not url:
            self.set_status(400)
            source = {"id": source_id, "name": name, "url": url, "request_headers": request_headers, "method": method, "enabled": enabled, "description": description}
            return self.render("admin/watchtower_source_edit.html", 
                              title="瞭望源管理", 
                              username=self.current_user,
                              source=source,
                              error="名称和URL为必填项")
        
        if source_id and source_id != "new":
            WatchtowerSourceRepository.update_source(source_id, name, url, request_headers, method, enabled, description)
        else:
            WatchtowerSourceRepository.create_source(name, url, request_headers, method, enabled, description)
        
        self.redirect("/admin/watchtower-sources")


class WatchtowerSourceDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, source_id):
        WatchtowerSourceRepository.delete_source(source_id)
        self.redirect("/admin/watchtower-sources")
