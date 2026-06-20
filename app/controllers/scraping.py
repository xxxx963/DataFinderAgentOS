import tornado.web
from app.controllers.base import BaseHandler
from app.models.system import (
    ScrapingSourceRepository, 
    ScrapedDataRepository,
    DeepScrapedDataRepository,
    DeepScrapeLogRepository,
    ModelEngineRepository
)
import math
import json
import httpx
from bs4 import BeautifulSoup
import time
import asyncio


class ScrapingSourceListHandler(BaseHandler):
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
        
        sources = ScrapingSourceRepository.get_all(page, page_size, keyword)
        total = ScrapingSourceRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/scraping_sources.html", 
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


class ScrapingSourceEditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, source_id=None):
        source = None
        
        if source_id and source_id != "new":
            source = ScrapingSourceRepository.get_by_id(source_id)
            if source and source["request_headers"]:
                try:
                    source = dict(source)
                    source["request_headers"] = json.loads(source["request_headers"])
                except:
                    source = dict(source)
        
        self.render("admin/scraping_source_edit.html", 
                    title="瞭望源管理", 
                    username=self.current_user,
                    source=source,
                    error=None)
    
    @tornado.web.authenticated
    def post(self, source_id=None):
        name = self.get_body_argument("name", "")
        url = self.get_body_argument("url", "")
        method = self.get_body_argument("method", "GET")
        enabled = self.get_body_argument("enabled", "1")
        description = self.get_body_argument("description", "")
        
        headers_input = self.get_body_argument("request_headers", "")
        try:
            request_headers = json.loads(headers_input) if headers_input else {}
        except:
            request_headers = {}
        
        try:
            enabled = int(enabled)
        except:
            enabled = 1
        
        if not name or not url:
            self.set_status(400)
            return self.render("admin/scraping_source_edit.html", 
                              title="瞭望源管理", 
                              username=self.current_user,
                              source={"id": source_id, "name": name, "url": url, "method": method, 
                                      "enabled": enabled, "description": description, "request_headers": request_headers},
                              error="请填写名称和URL")
        
        if source_id and source_id != "new":
            ScrapingSourceRepository.update(source_id, name, url, request_headers, method, enabled, description)
        else:
            ScrapingSourceRepository.create(name, url, request_headers, method, enabled, description)
        
        self.redirect("/admin/scraping-sources")


class ScrapingSourceDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, source_id):
        ScrapingSourceRepository.delete(source_id)
        self.redirect("/admin/scraping-sources")


class ScrapingHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        sources = ScrapingSourceRepository.get_enabled_sources()
        self.render("admin/scraping.html", 
                    title="瞭望采集", 
                    username=self.current_user,
                    sources=sources)
    
    @tornado.web.authenticated
    def post(self):
        keyword = self.get_body_argument("keyword", "")
        source_ids = self.get_body_arguments("source_ids")
        limit = self.get_body_argument("limit", "10")
        page = self.get_body_argument("page", "1")
        
        try:
            limit = int(limit)
            page = int(page)
        except:
            limit = 10
            page = 1
        
        if not keyword:
            self.write({"success": False, "error": "请输入搜索关键词"})
            return
        
        results = []
        for source_id in source_ids:
            try:
                source = ScrapingSourceRepository.get_by_id(source_id)
                if not source:
                    continue
                
                url = source["url"]
                if '{keyword}' in url:
                    url = url.replace('{keyword}', keyword)
                elif '%E8%A5%BF%E5%8D%8E%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6' in url:
                    import urllib.parse
                    url = url.replace('%E8%A5%BF%E5%8D%8E%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6', urllib.parse.quote(keyword))
                
                headers = {}
                if source["request_headers"]:
                    try:
                        headers = json.loads(source["request_headers"])
                    except:
                        pass
                
                response = httpx.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                if 'baidu.com' in url:
                    news_items = soup.select('.result-op.c-container.xpath-log.new-pmd')
                    for item in news_items[:limit]:
                        title_elem = item.select_one('h3 a')
                        url_elem = item.select_one('h3 a')
                        summary_elem = item.select_one('.c-abstract')
                        image_elem = item.select_one('.c-img')
                        
                        if title_elem and url_elem:
                            results.append({
                                'source_id': source_id,
                                'source_name': source["name"],
                                'title': title_elem.get_text(strip=True),
                                'url': url_elem['href'],
                                'summary': summary_elem.get_text(strip=True) if summary_elem else '',
                                'image_url': image_elem['src'] if image_elem else ''
                            })
                else:
                    links = soup.find_all('a', href=True)
                    for link in links[:limit]:
                        if link.get_text(strip=True):
                            results.append({
                                'source_id': source_id,
                                'source_name': source["name"],
                                'title': link.get_text(strip=True),
                                'url': link['href'],
                                'summary': '',
                                'image_url': ''
                            })
            except Exception as e:
                continue
        
        self.write({"success": True, "results": results})


class ScrapingSaveHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        items = self.get_body_argument("items", "")
        try:
            items = json.loads(items)
        except:
            self.write({"success": False, "error": "数据格式错误"})
            return
        
        saved_count = 0
        for item in items:
            try:
                ScrapedDataRepository.create(
                    source_id=item["source_id"],
                    title=item["title"],
                    url=item["url"],
                    summary=item.get("summary", ""),
                    image_url=item.get("image_url", "")
                )
                saved_count += 1
            except:
                continue
        
        self.write({"success": True, "saved_count": saved_count})


class ScrapedDataListHandler(BaseHandler):
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
        
        data_list = ScrapedDataRepository.get_all(page, page_size, keyword)
        total = ScrapedDataRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        
        # 准备分页数据
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        self.render("admin/scraped_data.html", 
                    title="数据仓库", 
                    username=self.current_user,
                    data_list=data_list,
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


class ScrapedDataDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, data_id):
        ScrapedDataRepository.delete_data(data_id)
        self.redirect("/admin/scraped-data")


class ScrapedDataDeleteMultipleHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        data_ids = self.get_body_arguments("data_ids")
        if data_ids:
            data_ids = [int(did) for did in data_ids if did]
            ScrapedDataRepository.delete_multiple_data(data_ids)
        self.redirect("/admin/scraped-data")


class WatchtowerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        sources = ScrapingSourceRepository.get_all(1, 1000, "")
        self.render("admin/watchtower.html", 
                    title="瞭望管理", 
                    username=self.current_user,
                    sources=sources)


class DeepScrapeHandler(BaseHandler):
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
        
        data_list = DeepScrapedDataRepository.get_all(page, page_size, keyword)
        total = DeepScrapedDataRepository.count(keyword)
        total_pages = int(math.ceil(float(total) / page_size)) if total > 0 else 1
        
        show_pagination = total_pages > 1
        has_prev = page > 1
        has_next = page < total_pages
        prev_page = page - 1
        next_page = page + 1
        page_numbers = list(range(1, total_pages + 1))
        
        statistics = DeepScrapedDataRepository.get_statistics()
        
        self.render("admin/deep_scrape.html", 
                    title="深度采集", 
                    username=self.current_user,
                    data_list=data_list,
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
                    statistics=statistics,
                    error=None)


class DeepScrapeExecuteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        data_ids = self.get_body_arguments("data_ids")
        results = []
        
        if not data_ids:
            self.write({"success": False, "error": "请选择要深度采集的数据"})
            return
        
        for data_id_str in data_ids:
            try:
                data_id = int(data_id_str)
                result = self._execute_deep_scrape(data_id)
                results.append(result)
            except Exception as e:
                results.append({
                    "data_id": data_id_str,
                    "success": False,
                    "error": str(e)
                })
        
        success_count = sum(1 for r in results if r["success"])
        self.write({
            "success": True,
            "total": len(results),
            "success_count": success_count,
            "results": results
        })
    
    def _execute_deep_scrape(self, data_id):
        scraped_data = ScrapedDataRepository.get_by_id(data_id)
        if not scraped_data:
            return {"data_id": data_id, "success": False, "error": "数据不存在"}
        
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_id = DeepScrapeLogRepository.create(
            scraped_data_id=data_id,
            status="running",
            message="开始深度采集",
            start_time=start_time
        )
        
        try:
            raw_content = self._fetch_webpage_content(scraped_data["url"])
            
            model_engine = ModelEngineRepository.get_default()
            if model_engine:
                analysis = self._analyze_with_model(model_engine, raw_content, scraped_data["title"])
            else:
                analysis = {
                    "summary": scraped_data["summary"] or "",
                    "key_points": [],
                    "entities": [],
                    "sentiment": "neutral"
                }
            
            DeepScrapedDataRepository.create(
                scraped_data_id=data_id,
                title=scraped_data["title"],
                url=scraped_data["url"],
                raw_content=raw_content,
                structured_content=analysis.get("structured", ""),
                key_points=json.dumps(analysis.get("key_points", [])),
                entities=json.dumps(analysis.get("entities", [])),
                sentiment=analysis.get("sentiment", "neutral"),
                summary=analysis.get("summary", scraped_data["summary"] or ""),
                full_text=raw_content,
                metadata=json.dumps({
                    "source": scraped_data.get("source_name", ""),
                    "scraped_at": scraped_data.get("scraped_at", "")
                })
            )
            
            ScrapedDataRepository.update_deep_scraped(data_id, 1)
            
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            DeepScrapeLogRepository.update(
                log_id,
                status="success",
                message="深度采集完成",
                end_time=end_time,
                tokens_used=analysis.get("tokens_used", 0)
            )
            
            return {
                "data_id": data_id,
                "success": True,
                "message": "采集完成"
            }
        except Exception as e:
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            DeepScrapeLogRepository.update(
                log_id,
                status="failed",
                message="深度采集失败",
                end_time=end_time,
                error_message=str(e)
            )
            return {
                "data_id": data_id,
                "success": False,
                "error": str(e)
            }
    
    def _fetch_webpage_content(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
            }
            response = httpx.get(url, headers=headers, timeout=30, follow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except:
            return ""
    
    def _analyze_with_model(self, model_engine, raw_content, title):
        try:
            import httpx
            import json
            
            system_prompt = """你是一个专业的数据分析助手。请对提供的网页内容进行分析，并返回以下格式的JSON：
{
    "summary": "内容摘要，不超过500字",
    "key_points": ["关键点1", "关键点2", "关键点3"],
    "entities": [{"name": "实体名", "type": "实体类型"}],
    "sentiment": "positive/negative/neutral"
}
"""
            
            prompt = f"标题: {title}\n\n内容: {raw_content[:8000]}"
            
            url = f"{model_engine['base_url'].rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {model_engine['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model_engine["model_name"],
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": model_engine.get("temperature", 0.7),
                "max_tokens": model_engine.get("max_tokens", 2048)
            }
            
            response = httpx.post(url, json=data, headers=headers, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            try:
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    analysis = json.loads(content[json_start:json_end])
                else:
                    analysis = {
                        "summary": content[:500],
                        "key_points": [],
                        "entities": [],
                        "sentiment": "neutral"
                    }
            except:
                analysis = {
                    "summary": content[:500],
                    "key_points": [],
                    "entities": [],
                    "sentiment": "neutral"
                }
            
            usage = result.get("usage", {})
            analysis["tokens_used"] = usage.get("total_tokens", 0)
            
            return analysis
        except:
            return {
                "summary": "",
                "key_points": [],
                "entities": [],
                "sentiment": "neutral",
                "tokens_used": 0
            }


class DeepScrapeDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, data_id):
        data = DeepScrapedDataRepository.get_by_id(data_id)
        if not data:
            self.redirect("/admin/deep-scrape")
            return
        
        logs = DeepScrapeLogRepository.get_all(1, 10, data["scraped_data_id"])
        
        self.render("admin/deep_scrape_detail.html", 
                    title="深度采集详情", 
                    username=self.current_user,
                    data=data,
                    logs=logs)


class DeepScrapeDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, data_id):
        DeepScrapedDataRepository.delete(data_id)
        self.redirect("/admin/deep-scrape")


from datetime import datetime