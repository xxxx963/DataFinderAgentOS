import tornado.web
import json
import csv
import io
from datetime import datetime
from app.controllers.base import BaseHandler
from app.models.system import ReportRepository


class ReportHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/report.html", title="问答报表统计", username=self.current_user)


class ReportExportHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        start_date = self.get_argument("start_date", "")
        end_date = self.get_argument("end_date", "")
        
        # 获取数据
        overview = ReportRepository.get_chat_statistics(start_date, end_date)
        daily_stats = ReportRepository.get_daily_statistics(7)
        category_stats = ReportRepository.get_skill_usage_statistics(start_date, end_date)
        top_questions = ReportRepository.get_top_questions(10, start_date, end_date)
        
        # 创建CSV内容
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入标题信息
        writer.writerow(['问答统计报表'])
        writer.writerow(['生成时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        if start_date:
            writer.writerow(['开始日期', start_date])
        if end_date:
            writer.writerow(['结束日期', end_date])
        writer.writerow([])
        
        # 写入概览统计
        writer.writerow(['概览统计'])
        writer.writerow(['总会话数', overview['total_conversations']])
        writer.writerow(['总消息数', overview['total_messages']])
        writer.writerow(['活跃用户', overview['active_users']])
        writer.writerow([])
        
        # 写入每日统计
        writer.writerow(['每日统计'])
        writer.writerow(['日期', '会话数'])
        for item in daily_stats:
            writer.writerow([item['date'], item['conversations']])
        writer.writerow([])
        
        # 写入分类统计
        writer.writerow(['问题分类统计'])
        writer.writerow(['分类', '数量'])
        for item in category_stats:
            writer.writerow([item['category'], item['count']])
        writer.writerow([])
        
        # 写入高频问题
        writer.writerow(['高频问题 TOP 10'])
        writer.writerow(['排名', '问题', '次数'])
        for i, item in enumerate(top_questions, 1):
            writer.writerow([i, item['question'], item['frequency']])
        
        # 设置响应头
        self.set_header("Content-Type", "text/csv; charset=utf-8")
        self.set_header("Content-Disposition", f"attachment; filename=report_{datetime.now().strftime('%Y%m%d')}.csv")
        self.write(output.getvalue())


class ReportApiHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        report_type = self.get_argument("type", "overview")
        start_date = self.get_argument("start_date", "")
        end_date = self.get_argument("end_date", "")
        
        result = {}
        
        if report_type == "overview":
            stats = ReportRepository.get_chat_statistics(start_date, end_date)
            message_types = ReportRepository.get_message_type_statistics(start_date, end_date)
            result = {
                "total_conversations": stats["total_conversations"],
                "total_messages": stats["total_messages"],
                "active_users": stats["active_users"],
                "message_types": message_types
            }
        
        elif report_type == "daily":
            days = self.get_argument("days", 7)
            try:
                days = int(days)
            except:
                days = 7
            result = ReportRepository.get_daily_statistics(days)
        
        elif report_type == "hourly":
            result = ReportRepository.get_hourly_statistics()
        
        elif report_type == "top_questions":
            limit = self.get_argument("limit", 10)
            try:
                limit = int(limit)
            except:
                limit = 10
            result = ReportRepository.get_top_questions(limit, start_date, end_date)
        
        elif report_type == "user_stats":
            limit = self.get_argument("limit", 10)
            try:
                limit = int(limit)
            except:
                limit = 10
            result = ReportRepository.get_user_statistics(limit)
        
        elif report_type == "weekly":
            weeks = self.get_argument("weeks", 4)
            try:
                weeks = int(weeks)
            except:
                weeks = 4
            result = ReportRepository.get_weekly_statistics(weeks)
        
        elif report_type == "category":
            result = ReportRepository.get_skill_usage_statistics(start_date, end_date)
        
        elif report_type == "skill_bar":
            result = ReportRepository.get_skill_usage_bar(start_date, end_date)
        
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))