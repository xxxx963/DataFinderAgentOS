import os
import tornado.web
import tornado.gen
import json
import asyncio
import requests
import re
from app.controllers.base import BaseHandler
from app.models.user import UserRepository
from app.models.system import (
    ConversationRepository,
    ConversationMessageRepository,
    ModelEngineRepository,
    SkillRepository,
    DigitalEmployeeRepository
)
from app.models.db import get_connection

# 西师妹配置（从环境变量读取）
XISHIMEI_API_KEY = os.environ.get("XISHIMEI_API_KEY", "")
XISHIMEI_BASE_URL = os.environ.get("XISHIMEI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
XISHIMEI_MODEL_NAME = os.environ.get("XISHIMEI_MODEL_NAME", "qwen3.5-flash")

XISHIMEI_PROMPT = """
你是西师妹，西华师范大学专属温柔校园数字助手。
只解答西华师范大学相关问题：校区地址、专业、招生分数线、校史、社团、实训、南充校园生活。
用户只发送空白提问时，引导用户说出校内相关疑问；
如果询问校外无关内容，礼貌告知仅能解答西华师大相关问题。
"""

# 天气助手配置（从环境变量读取）
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")
WEATHER_BASE_URL = os.environ.get("WEATHER_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
WEATHER_MODEL_NAME = os.environ.get("WEATHER_MODEL_NAME", "qwen3.5-flash")

# 音乐助手配置（从环境变量读取）
MUSIC_API_KEY = os.environ.get("MUSIC_API_KEY", "")
MUSIC_BASE_URL = os.environ.get("MUSIC_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
MUSIC_MODEL_NAME = os.environ.get("MUSIC_MODEL_NAME", "qwen3.5-flash")

# 音乐数据库（使用Web Audio API生成音乐）
MUSIC_DATABASE = {
    "晴天": {"artist": "周杰伦", "pattern": "happy"},
    "稻香": {"artist": "周杰伦", "pattern": "nature"},
    "夜曲": {"artist": "周杰伦", "pattern": "night"},
    "告白气球": {"artist": "周杰伦", "pattern": "love"},
    "七里香": {"artist": "周杰伦", "pattern": "romantic"},
    "成都": {"artist": "赵雷", "pattern": "folk"},
    "南方姑娘": {"artist": "赵雷", "pattern": "gentle"},
    "平凡之路": {"artist": "朴树", "pattern": "road"},
    "起风了": {"artist": "买辣椒也用券", "pattern": "wind"},
    "往后余生": {"artist": "马良", "pattern": "life"},
    "刚好遇见你": {"artist": "李玉刚", "pattern": "meet"},
    "凉凉": {"artist": "杨宗纬&张碧晨", "pattern": "cool"},
    "体面": {"artist": "于文文", "pattern": "elegant"},
    "追光者": {"artist": "岑宁儿", "pattern": "light"},
    "消愁": {"artist": "毛不易", "pattern": "sad"},
    "像我这样的人": {"artist": "毛不易", "pattern": "person"},
    "后来": {"artist": "刘若英", "pattern": "memory"},
    "成全": {"artist": "林宥嘉", "pattern": "complete"},
    "可惜没如果": {"artist": "林俊杰", "pattern": "regret"},
    "遇见": {"artist": "孙燕姿", "pattern": "encounter"},
}

MUSIC_PROMPT = """
你是音乐小助手，专门为用户提供音乐相关的服务。

你可以：
- 搜索歌曲
- 推荐音乐
- 提供歌手信息
- 回答音乐相关问题

请保持友好、简洁的回答风格。
"""

# 实时天气API配置（使用Open-Meteo免费API）
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# 城市坐标映射
CITY_COORDS = {
    "北京": {"lat": 39.9042, "lon": 116.4074},
    "上海": {"lat": 31.2304, "lon": 121.4737},
    "广州": {"lat": 23.1291, "lon": 113.2644},
    "成都": {"lat": 30.5728, "lon": 104.0668},
    "南充": {"lat": 30.8374, "lon": 106.1147},
    "深圳": {"lat": 22.5431, "lon": 114.0579},
    "杭州": {"lat": 30.2741, "lon": 120.1552},
    "重庆": {"lat": 29.4316, "lon": 106.9123},
    "武汉": {"lat": 30.5928, "lon": 114.3055},
    "西安": {"lat": 34.2619, "lon": 108.9463},
    "南京": {"lat": 32.0603, "lon": 118.7969},
    "天津": {"lat": 39.1256, "lon": 117.2264},
    "苏州": {"lat": 31.3251, "lon": 120.6196},
    "郑州": {"lat": 34.7466, "lon": 113.6253},
    "长沙": {"lat": 28.2281, "lon": 112.9388},
    "青岛": {"lat": 36.0671, "lon": 120.3826},
    "沈阳": {"lat": 41.8045, "lon": 123.4315},
    "大连": {"lat": 38.9140, "lon": 121.6147},
    "厦门": {"lat": 24.4798, "lon": 118.0894},
    "哈尔滨": {"lat": 45.8038, "lon": 126.5349}
}

WEATHER_PROMPT = """
你是天气小助手，专门为用户提供天气相关的查询和建议。

你可以回答以下类型的问题：
- 查询当前天气状况
- 查询未来天气预报
- 提供穿衣建议
- 提醒天气变化注意事项
- 解释天气现象
- 提供空气质量信息

回答时请保持友好、简洁，如果没有具体城市信息，可以询问用户想查询哪个城市的天气。
如果用户的问题与天气无关，请礼貌地说明你只能回答天气相关问题。
"""


class ChatHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("web/chat.html", title="AI 问数", username=self.current_user)


class ModelsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        models = ModelEngineRepository.get_all(1, 100)
        result = []
        for model in models:
            result.append({
                "id": model["id"],
                "name": model["name"],
                "is_default": model["is_default"] == 1
            })
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))


class SkillsApiHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        SkillRepository.init_default_skills()
        
        skills = SkillRepository.get_enabled()
        result = []
        for skill in skills:
            result.append({
                "id": skill["id"],
                "identifier": skill["skill_identifier"],
                "name": skill["name"],
                "description": skill["description"] or "",
                "skill_type": skill["skill_type"]
            })
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))


class DigitalEmployeesHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        employees = DigitalEmployeeRepository.get_all()
        result = []
        for employee in employees:
            result.append({
                "id": employee["id"],
                "name": employee["name"],
                "description": employee["description"],
                "avatar": employee.get("avatar", "🤖"),
                "enable_switch_model": employee["enable_switch_model"] == 1,
                "enable_play_music": employee["enable_play_music"] == 1,
                "enable_view_history": employee["enable_view_history"] == 1
            })
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))


class ConversationsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        user = UserRepository.get_user_by_username(username)
        if not user:
            self.set_status(404)
            return
        
        conversations = ConversationRepository.get_all_by_user(user["id"], 1, 50)
        result = []
        for conv in conversations:
            result.append({
                "id": conv["id"],
                "title": conv["title"],
                "model_engine_id": conv["model_engine_id"],
                "created_at": conv["created_at"],
                "updated_at": conv["updated_at"]
            })
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))


class ConversationDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, conversation_id):
        try:
            conv_id = int(conversation_id)
        except:
            self.set_status(400)
            return
        
        conversation = ConversationRepository.get_by_id(conv_id)
        if not conversation:
            self.set_status(404)
            return
        
        messages = ConversationMessageRepository.get_by_conversation(conv_id)
        result = {
            "id": conversation["id"],
            "title": conversation["title"],
            "messages": []
        }
        
        for msg in messages:
            result["messages"].append({
                "role": msg["role"],
                "content": msg["content"],
                "created_at": msg["created_at"]
            })
        
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))


class ChatStreamHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        message = self.get_argument("message", "")
        conversation_id_str = self.get_argument("conversation_id", "")
        model_id_str = self.get_argument("model_id", "")
        
        if not message:
            self.set_status(400)
            return
        
        username = self.current_user
        user = UserRepository.get_user_by_username(username)
        if not user:
            self.set_status(401)
            return
        
        conversation_id = None
        if conversation_id_str:
            try:
                conversation_id = int(conversation_id_str)
            except:
                pass
        
        model_id = None
        if model_id_str:
            try:
                model_id = int(model_id_str)
            except:
                pass
        
        # 获取或创建对话
        if not conversation_id:
            title = message[:30] + "..." if len(message) > 30 else message
            conversation_id = ConversationRepository.create(user["id"], title, model_id)
        else:
            # 更新对话时间
            ConversationRepository.update(conversation_id)
        
        # 保存用户消息
        ConversationMessageRepository.create(conversation_id, "user", message)
        
        # 设置 SSE 响应头
        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Connection", "keep-alive")
        
        # 发送会话 ID
        self.write(f"data: {json.dumps({'conversation_id': conversation_id})}\n\n")
        self.flush()
        
        # 获取模型配置
        model_engine = None
        if model_id:
            model_engine = ModelEngineRepository.get_by_id(model_id)
        
        if not model_engine:
            model_engine = ModelEngineRepository.get_default()
        
        # 处理消息
        await self.process_message(message, conversation_id, model_engine)
    
    async def process_message(self, message, conversation_id, model_engine):
        print(f"\n=== 处理消息 ===")
        print(f"消息内容: {message}")
        
        # 意图识别
        intent = self.recognize_intent(message)
        print(f"识别到的意图: {intent}")
        
        # 根据意图处理
        if intent.startswith("skill_"):
            skill_identifier = intent.replace("skill_", "")
            skill_input = message.strip()[1:]
            skill_input = skill_input[len(skill_identifier):].strip()
            print(f"路由到技能处理: /{skill_identifier} input={skill_input}")
            
            if skill_identifier == "search":
                await self.handle_skill_search(skill_input, conversation_id, model_engine)
            elif skill_identifier == "sql":
                await self.handle_skill_sql(skill_input, conversation_id, model_engine)
            elif skill_identifier == "stat":
                await self.handle_skill_stat(skill_input, conversation_id, model_engine)
            elif skill_identifier == "help":
                await self.handle_skill_help(skill_input, conversation_id, model_engine)
            elif skill_identifier == "model":
                await self.handle_skill_model(skill_input, conversation_id, model_engine)
            return
        
        if intent == "xishimei":
            print(f"路由到西师妹处理")
            await self.handle_xishimei_chat(message, conversation_id)
        elif intent == "weather":
            await self.handle_weather_chat(message, conversation_id)
        elif intent == "music":
            await self.handle_music_chat(message, conversation_id, model_engine)
        elif intent == "database_query":
            await self.handle_database_query(message, conversation_id, model_engine)
        elif intent == "deep_analysis":
            await self.handle_deep_analysis(message, conversation_id, model_engine)
        elif intent == "general_employee":
            await self.handle_general_chat(message, conversation_id, model_engine)
        else:
            await self.handle_general_chat(message, conversation_id, model_engine)
    
    def recognize_intent(self, message):
        # 首先检查是否是技能指令调度（优先级最高）
        skill_pattern = re.match(r'^/(\w+)\s*(.*)$', message.strip(), re.DOTALL)
        if skill_pattern:
            skill_identifier = skill_pattern.group(1).lower()
            valid_skills = ['search', 'sql', 'stat', 'help', 'model']
            if skill_identifier in valid_skills:
                return f"skill_{skill_identifier}"
        
        # 检查是否包含数字员工调用（格式：@员工名称）
        employee_match = re.match(r'@(\S+)', message)
        if employee_match:
            employee_name = employee_match.group(1)
            if employee_name == "西师妹":
                return "xishimei"
            elif employee_name == "天气":
                return "weather"
            elif employee_name == "音乐":
                return "music"
            else:
                return "general_employee"
        
        # 数据库查询意图
        lower_message = message.lower()
        db_keywords = ["数据库", "查询", "数据", "统计", "分析", "有多少", "显示"]
        if any(keyword in lower_message for keyword in db_keywords):
            return "database_query"
        
        # 深度分析意图
        analysis_keywords = ["深度", "分析", "详细", "深入"]
        if any(keyword in lower_message for keyword in analysis_keywords):
            return "deep_analysis"
        
        return "general"
    
    async def handle_xishimei_chat(self, message, conversation_id):
        print(f"=== 西师妹请求 ===")
        print(f"原始消息: {message}")
        
        # 去除@西师妹标记
        clean_message = message.replace("@西师妹", "").strip()
        print(f"清理后的消息: {clean_message}")
        
        # 如果用户只发送了@西师妹，没有附加问题，引导用户提问
        if not clean_message:
            response_content = "你好呀！我是西华师范大学专属的西师妹～\n\n请问有什么关于学校的问题想要问我吗？比如：\n- 🏫 校区地址\n- 📚 本科专业\n- 🎓 招生分数线\n- 📖 校史介绍\n- 👥 社团活动\n- 🍽️ 校园生活"
            print(f"发送引导消息")
            await self.send_response_stream(response_content, conversation_id)
            return
        
        # 构建消息列表
        msg_list = [{"role": "system", "content": XISHIMEI_PROMPT}]
        
        # 获取历史消息
        history = ConversationMessageRepository.get_by_conversation(conversation_id)
        for msg in history:
            # 只添加@西师妹相关的消息
            if "@西师妹" in msg["content"]:
                clean_content = msg["content"].replace("@西师妹", "").strip()
                msg_list.append({"role": msg["role"], "content": clean_content})
        
        msg_list.append({"role": "user", "content": clean_message})
        
        try:
            # 调用西师妹模型
            url = f"{XISHIMEI_BASE_URL.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {XISHIMEI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": XISHIMEI_MODEL_NAME,
                "messages": msg_list,
                "temperature": 0.7,
                "max_tokens": 2048,
                "stream": True
            }
            
            print(f"正在调用西师妹 API...")
            print(f"URL: {url}")
            print(f"模型: {XISHIMEI_MODEL_NAME}")
            
            # 使用 requests 同步调用，获取所有数据
            def call_api():
                try:
                    with requests.post(url, headers=headers, json=data, stream=True, timeout=60) as response:
                        response.raise_for_status()
                        result = ""
                        chunks = []
                        for line in response.iter_lines():
                            if line:
                                line_str = line.decode('utf-8')
                                if line_str.startswith('data: '):
                                    try:
                                        json_data = line_str[6:]
                                        if json_data == '[DONE]':
                                            break
                                        data_obj = json.loads(json_data)
                                        if data_obj.get('choices') and data_obj['choices'][0].get('delta'):
                                            content = data_obj['choices'][0]['delta'].get('content', '')
                                            if content:
                                                result += content
                                                chunks.append(content)
                                    except Exception as e:
                                        pass
                        return result, chunks
                except Exception as e:
                    print(f"西师妹 API 调用失败: {e}")
                    raise
            
            # 在 executor 中运行同步调用
            response_content, chunks = await asyncio.get_event_loop().run_in_executor(None, call_api)
            
            # 在异步上下文中发送流式响应
            for content in chunks:
                self.write(f"data: {json.dumps({'content': content})}\n\n")
                self.flush()
            
            # 保存 AI 响应
            ConversationMessageRepository.create(conversation_id, "assistant", response_content)
            
            # 发送完成信号
            self.write("data: [DONE]\n\n")
            self.flush()
            
        except Exception as e:
            error_content = f"抱歉，西师妹暂时无法回答您的问题：{str(e)}"
            print(f"西师妹错误: {e}")
            await self.send_response_stream(error_content, conversation_id)
    
    def extract_city(self, message):
        """从消息中提取城市名称"""
        for city in CITY_COORDS.keys():
            if city in message:
                return city
        return None
    
    async def get_real_time_weather(self, city):
        """获取实时天气数据"""
        if city not in CITY_COORDS:
            return None
        
        coords = CITY_COORDS[city]
        try:
            # 使用 requests 同步调用
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
                "hourly": "temperature_2m,weather_code",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min",
                "forecast_days": 3,
                "timezone": "Asia/Shanghai"
            }
            response = requests.get(OPEN_METEO_URL, params=params, timeout=30)
            return response.json()
        except Exception as e:
            print(f"获取天气数据失败: {e}")
            return None
    
    def format_weather_response(self, city, weather_data):
        """格式化天气响应"""
        if not weather_data:
            return None
        
        weather_codes = {
            0: "晴天",
            1: "晴",
            2: "多云",
            3: "阴天",
            45: "雾",
            48: "霜",
            51: "小雨",
            53: "中雨",
            55: "大雨",
            61: "阵雨",
            63: "阵雨",
            65: "雷阵雨",
            71: "小雪",
            73: "中雪",
            75: "大雪",
            80: "阵雨",
            81: "阵雨",
            82: "暴雨",
            95: "雷暴",
            96: "雷暴伴冰雹",
            99: "雷暴伴冰雹"
        }
        
        current = weather_data.get("current", {})
        daily = weather_data.get("daily", {})
        
        temp = current.get("temperature_2m", "N/A")
        feels_like = current.get("apparent_temperature", "N/A")
        humidity = current.get("relative_humidity_2m", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")
        weather_code = current.get("weather_code", 0)
        weather_desc = weather_codes.get(weather_code, "未知天气")
        
        today_high = daily.get("temperature_2m_max", ["N/A"])[0]
        today_low = daily.get("temperature_2m_min", ["N/A"])[0]
        
        response = f"🌤️ **{city}今日天气**\n\n"
        response += f"天气状况：{weather_desc}\n"
        response += f"当前温度：{temp}°C（体感温度：{feels_like}°C）\n"
        response += f"今日气温：{today_low}°C ~ {today_high}°C\n"
        response += f"相对湿度：{humidity}%\n"
        response += f"风速：{wind_speed} km/h\n\n"
        
        # 穿衣建议
        if isinstance(temp, (int, float)):
            if temp < 10:
                response += "🧥 穿衣建议：建议穿羽绒服、厚外套等保暖衣物"
            elif temp < 15:
                response += "🧥 穿衣建议：建议穿毛衣、外套"
            elif temp < 20:
                response += "👕 穿衣建议：建议穿长袖衬衫、薄外套"
            elif temp < 25:
                response += "👕 穿衣建议：建议穿短袖、薄长裤"
            else:
                response += "🩳 穿衣建议：建议穿短袖短裤等清凉衣物"
        
        return response
    
    async def handle_weather_chat(self, message, conversation_id):
        # 去除@天气标记
        clean_message = message.replace("@天气", "").strip()
        
        # 如果用户只发送了@天气，没有附加问题，引导用户提问
        if not clean_message:
            response_content = "你好呀！我是天气小助手～\n\n请问你想查询哪个城市的天气？比如：\n- 🌤️ 北京今天天气怎么样？\n- 🌧️ 上海明天会下雨吗？\n- 🌡️ 广州的气温是多少？\n- 🧥 今天适合穿什么衣服？"
            await self.send_response_stream(response_content, conversation_id)
            return
        
        # 尝试提取城市名称并获取实时天气
        city = self.extract_city(clean_message)
        
        if city:
            weather_data = await self.get_real_time_weather(city)
            if weather_data:
                real_time_response = self.format_weather_response(city, weather_data)
                if real_time_response:
                    await self.send_response_stream(real_time_response, conversation_id)
                    return
        
        # 如果无法获取实时天气，使用AI回答
        # 构建消息列表
        msg_list = [{"role": "system", "content": WEATHER_PROMPT}]
        
        # 获取历史消息
        history = ConversationMessageRepository.get_by_conversation(conversation_id)
        for msg in history:
            # 只添加@天气相关的消息
            if "@天气" in msg["content"]:
                clean_content = msg["content"].replace("@天气", "").strip()
                msg_list.append({"role": msg["role"], "content": clean_content})
        
        msg_list.append({"role": "user", "content": clean_message})
        
        try:
            # 调用天气模型
            url = f"{WEATHER_BASE_URL.rstrip('/')}/chat/completions"
            headers = {
                "Authorization": f"Bearer {WEATHER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": WEATHER_MODEL_NAME,
                "messages": msg_list,
                "temperature": 0.7,
                "max_tokens": 2048,
                "stream": True
            }
            
            # 使用 requests 同步调用，获取所有数据
            def call_api():
                try:
                    with requests.post(url, headers=headers, json=data, stream=True, timeout=60) as response:
                        response.raise_for_status()
                        result = ""
                        chunks = []
                        for line in response.iter_lines():
                            if line:
                                line_str = line.decode('utf-8')
                                if line_str.startswith('data: '):
                                    try:
                                        json_data = line_str[6:]
                                        if json_data == '[DONE]':
                                            break
                                        data_obj = json.loads(json_data)
                                        if data_obj.get('choices') and data_obj['choices'][0].get('delta'):
                                            content = data_obj['choices'][0]['delta'].get('content', '')
                                            if content:
                                                result += content
                                                chunks.append(content)
                                    except Exception as e:
                                        pass
                        return result, chunks
                except Exception as e:
                    print(f"天气 API 调用失败: {e}")
                    raise
            
            # 在 executor 中运行同步调用
            response_content, chunks = await asyncio.get_event_loop().run_in_executor(None, call_api)
            
            # 在异步上下文中发送流式响应
            for content in chunks:
                self.write(f"data: {json.dumps({'content': content})}\n\n")
                self.flush()
            
            # 保存 AI 响应
            ConversationMessageRepository.create(conversation_id, "assistant", response_content)
            
            # 发送完成信号
            self.write("data: [DONE]\n\n")
            self.flush()
            
        except Exception as e:
            error_content = f"抱歉，天气助手暂时无法回答您的问题：{str(e)}"
            print(f"天气错误: {e}")
            await self.send_response_stream(error_content, conversation_id)
    
    def search_music(self, keyword):
        """搜索音乐"""
        results = []
        keyword = keyword.lower()
        
        for song_name, info in MUSIC_DATABASE.items():
            if keyword in song_name.lower() or keyword in info["artist"].lower():
                results.append({
                    "name": song_name,
                    "artist": info["artist"],
                    "pattern": info["pattern"]
                })
        
        return results[:5]
    
    async def handle_music_chat(self, message, conversation_id, model_engine):
        # 去除@音乐标记
        clean_message = message.replace("@音乐", "").strip()
        
        # 如果用户只发送了@音乐，没有附加问题，引导用户提问
        if not clean_message:
            response_content = "🎶 你好呀！我是酷猫音乐小助手～\n\n请问你想找什么歌曲？比如：\n- 搜索周杰伦的歌\n- 播放晴天\n- 推荐一些好听的歌曲"
            await self.send_response_stream(response_content, conversation_id)
            return
        
        # 提取播放指令和关键词
        play_command = False
        search_keyword = clean_message
        
        # 检查是否包含播放指令
        if clean_message.startswith('播放'):
            play_command = True
            search_keyword = clean_message[2:].strip()
        elif clean_message.startswith('唱'):
            play_command = True
            search_keyword = clean_message[1:].strip()
        
        # 尝试搜索音乐
        results = self.search_music(search_keyword)
        
        if results:
            # 找到匹配的歌曲
            response_content = "🎵 为你找到以下歌曲：\n\n"
            for i, song in enumerate(results, 1):
                response_content += f"{i}. **{song['name']}** - {song['artist']}\n"
            
            # 如果只有一首匹配且包含播放指令，自动播放
            if len(results) == 1 and play_command:
                song = results[0]
                response_content += f"\n🎧 正在为你播放 **{song['name']}**...\n\n"
                response_content += f'<div class="music-card" data-song-name="{song["name"]}" data-song-artist="{song["artist"]}" data-song-pattern="{song["pattern"]}">'
                response_content += f'<div class="music-card-header"><div class="music-card-icon"><i class="fas fa-music"></i></div>'
                response_content += f'<div class="music-card-info"><div class="music-card-title">{song["name"]}</div>'
                response_content += f'<div class="music-card-artist">{song["artist"]}</div></div></div>'
                response_content += '<div class="music-card-controls"><button class="music-card-btn" onclick="playMusicByName(\'' + song["name"] + '\')">'
                response_content += '<i class="fas fa-play"></i> 立即播放</button></div></div>'
            else:
                response_content += "\n请告诉我你想播放哪一首，或者直接说「播放+歌曲名」～"
                
            await self.send_response_stream(response_content, conversation_id)
            return
        
        # 如果无法找到音乐，使用大模型回答音乐相关问题
        if model_engine:
            try:
                # 构建消息列表，包含音乐助手角色设定
                messages = [
                    {"role": "system", "content": MUSIC_PROMPT},
                    {"role": "user", "content": clean_message}
                ]
                
                # 调用大模型
                result = await self.call_model(model_engine, messages)
                response_content = f"🎵 {result}"
            except Exception as e:
                response_content = f"😔 没有找到包含「{search_keyword}」的歌曲\n\n试试这些热门歌曲：\n- 晴天 - 周杰伦\n- 成都 - 赵雷\n- 平凡之路 - 朴树\n- 起风了 - 买辣椒也用券\n\n或者直接说「播放+歌曲名」来播放音乐～"
        else:
            response_content = f"😔 没有找到包含「{search_keyword}」的歌曲\n\n试试这些热门歌曲：\n- 晴天 - 周杰伦\n- 成都 - 赵雷\n- 平凡之路 - 朴树\n- 起风了 - 买辣椒也用券\n\n或者直接说「播放+歌曲名」来播放音乐～"
        
        await self.send_response_stream(response_content, conversation_id)
    
    async def handle_general_chat(self, message, conversation_id, model_engine):
        response_content = ""
        
        # 获取历史消息
        history = ConversationMessageRepository.get_by_conversation(conversation_id)
        
        # 构建消息
        messages = []
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        if model_engine:
            try:
                # 调用模型
                result = await self.call_model(model_engine, messages)
                response_content = result
            except Exception as e:
                response_content = f"抱歉，发生了一些错误：{str(e)}"
        else:
            response_content = "请先配置模型引擎才能使用 AI 功能！"
        
        # 发送响应
        await self.send_response_stream(response_content, conversation_id)
    
    async def handle_database_query(self, message, conversation_id, model_engine):
        # 查询数据库中的数据
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM scraped_data")
            data_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM scraping_sources")
            source_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM deep_scraped_data")
            deep_count = cursor.fetchone()["count"]
        
        response_content = f"""## 数据库统计信息

当前数据库状态：
- 📊 采集数据：{data_count} 条
- 🔌 采集源：{source_count} 个
- 📝 深度分析：{deep_count} 条

### 最近采集的数据：
"""
        
        with get_connection() as conn:
            cursor = conn.execute("""
                SELECT s.title, s.url, s.created_at, src.name as source_name 
                FROM scraped_data s 
                LEFT JOIN scraping_sources src ON s.source_id = src.id 
                ORDER BY s.id DESC LIMIT 5
            """)
            recent_data = cursor.fetchall()
            
            for item in recent_data:
                title = item["title"] or "无标题"
                source = item["source_name"] or "未知来源"
                response_content += f"- **{title}** ({source})\n"
        
        await self.send_response_stream(response_content, conversation_id)
    
    async def handle_deep_analysis(self, message, conversation_id, model_engine):
        response_content = """## 深度分析功能

深度分析可以：
- 📊 进行数据统计和可视化
- 🧠 使用 AI 进行内容分析
- 📝 提取关键信息
- 🏷️ 智能标签和分类

如需使用深度分析，请在后台管理中配置好模型引擎后，选择数据进行深度采集！
"""
        await self.send_response_stream(response_content, conversation_id)
    
    async def call_model(self, model_engine, messages):
        try:
            base_url = model_engine['base_url'].rstrip('/')
            api_key = model_engine['api_key']
            model_name = model_engine['model_name']
            temperature = model_engine.get("temperature", 0.7)
            max_tokens = model_engine.get("max_tokens", 2048)
            
            if 'dashscope' in base_url or 'aliyuncs' in base_url:
                if 'compatible-mode' in base_url:
                    # OpenAI 兼容端点
                    url = f"{base_url}/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": model_name,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                else:
                    # DashScope 原生端点
                    url = base_url
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": model_name,
                        "input": {
                            "messages": messages
                        },
                        "parameters": {
                            "temperature": temperature,
                            "max_tokens": max_tokens
                        }
                    }
            else:
                url = f"{base_url}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            
            def call_api():
                response = requests.post(url, headers=headers, json=data, timeout=60)
                
                if response.status_code != 200:
                    raise Exception(f"API请求失败，状态码: {response.status_code}")
                
                result = response.json()
                
                if 'dashscope' in base_url or 'aliyuncs' in base_url:
                    if 'compatible-mode' in base_url:
                        # OpenAI 兼容端点响应格式
                        if "choices" not in result or not result["choices"]:
                            error_msg = result.get("error", {}).get("message", "未知错误") if "error" in result else "API响应格式不正确"
                            raise Exception(f"API响应不包含有效数据: {error_msg}")
                        if "message" not in result["choices"][0]:
                            raise Exception("API响应格式不正确，缺少message字段")
                        if "content" not in result["choices"][0]["message"]:
                            raise Exception("API响应格式不正确，缺少content字段")
                        return result["choices"][0]["message"]["content"]
                    else:
                        # DashScope 原生端点响应格式
                        if "output" not in result:
                            error_msg = result.get("error", {}).get("message", "未知错误") if "error" in result else "API响应格式不正确"
                            raise Exception(f"API响应不包含有效数据: {error_msg}")
                        return result["output"].get("text", "")
                else:
                    if "choices" not in result or not result["choices"]:
                        error_msg = result.get("error", {}).get("message", "未知错误") if "error" in result else "API响应格式不正确"
                        raise Exception(f"API响应不包含有效数据: {error_msg}")
                    
                    if "message" not in result["choices"][0]:
                        raise Exception("API响应格式不正确，缺少message字段")
                    
                    if "content" not in result["choices"][0]["message"]:
                        raise Exception("API响应格式不正确，缺少content字段")
                    
                    return result["choices"][0]["message"]["content"]
            
            return await asyncio.get_event_loop().run_in_executor(None, call_api)
        except Exception as e:
            print(f"调用模型失败: {str(e)}")
            return f"调用模型失败：{str(e)}"
    
    async def send_response_stream(self, content, conversation_id):
        # 逐字符发送
        response_text = ""
        for char in content:
            response_text += char
            self.write(f"data: {json.dumps({'content': char})}\n\n")
            self.flush()
            await asyncio.sleep(0.01)  # 稍微延迟，让效果更好
        
        # 保存 AI 响应
        ConversationMessageRepository.create(conversation_id, "assistant", content)
        
        # 发送完成信号
        self.write("data: [DONE]\n\n")
        self.flush()
    
    async def handle_skill_search(self, skill_input, conversation_id, model_engine):
        if not skill_input:
            response_content = """## 🌐 网络搜索技能

使用格式：`/search 关键词`

示例：
- `/search 人工智能最新发展`
- `/search Python编程教程`
- `/search 今日新闻`

请告诉我你想搜索什么内容？
"""
            await self.send_response_stream(response_content, conversation_id)
            return
        
        search_prompt = f"""你是一个网络搜索助手。请根据用户输入的关键词，帮助用户搜索相关信息。

用户想要搜索：{skill_input}

请生成3-5个相关的搜索建议或直接提供相关信息摘要。保持简洁明了。
"""
        
        if model_engine:
            try:
                messages = [{"role": "system", "content": search_prompt}, {"role": "user", "content": skill_input}]
                result = await self.call_model(model_engine, messages)
                response_content = f"""## 🌐 搜索结果

**关键词**: {skill_input}

{result}

---
*💡 提示：以上结果由 AI 生成，如有需要你可以进一步提问或使用 /sql 查询系统数据*
"""
            except Exception as e:
                response_content = f"搜索时发生错误：{str(e)}"
        else:
            response_content = "请先配置模型引擎才能使用搜索功能！"
        
        await self.send_response_stream(response_content, conversation_id)
    
    async def handle_skill_sql(self, skill_input, conversation_id, model_engine):
        if not skill_input:
            response_content = """## 📊 数据问数技能

使用格式：`/sql 查询需求`

示例：
- `/sql 查询最近采集的数据有多少条`
- `/sql 统计每个采集源的数据量`
- `/sql 查看最新的10条采集数据`

你可以用自然语言描述你的数据查询需求，我会帮你查询并返回结果。
"""
            await self.send_response_stream(response_content, conversation_id)
            return
        
        if model_engine:
            try:
                table_info = self.get_database_schema()
                
                sql_prompt = f"""你是一个数据分析师，擅长根据用户需求生成 SQL 查询语句。

数据库表结构：
{table_info}

用户需求：{skill_input}

请生成一条 SQLite SQL 查询语句来实现这个需求。只返回 SQL 语句，不要其他内容。
"""
                
                messages = [{"role": "system", "content": sql_prompt}, {"role": "user", "content": skill_input}]
                sql_result = await self.call_model(model_engine, messages)
                
                sql_query = sql_result.strip()
                if sql_query.startswith("```"):
                    lines = sql_query.split('\n')
                    sql_query = '\n'.join(lines[1:-1])
                sql_query = sql_query.strip()
                
                print(f"生成的SQL: {sql_query}")
                
                with get_connection() as conn:
                    try:
                        cursor = conn.execute(sql_query)
                        columns = [desc[0] for desc in cursor.description] if cursor.description else []
                        rows = cursor.fetchall()
                        
                        if not rows:
                            response_content = f"""## 📊 查询结果

**需求**: {skill_input}

**SQL**: `已安全处理，不向用户显示`

查询结果为空，没有找到匹配的数据。
"""
                        else:
                            result_rows = []
                            for row in rows[:20]:
                                result_rows.append(dict(row))
                            
                            response_content = f"""## 📊 查询结果

**需求**: {skill_input}

**结果**:
| {' | '.join(columns)} |
|{' | '.join(['---' for _ in columns])} |
"""
                            for row in result_rows:
                                values = [str(row[col]) if col in row else '' for col in columns]
                                response_content += f"| {' | '.join(values)} |\n"
                            
                            if len(rows) > 20:
                                response_content += f"\n*...共 {len(rows)} 条结果，仅显示前20条*\n"
                            else:
                                response_content += f"\n*共 {len(rows)} 条结果*\n"
                    
                    except Exception as sql_err:
                        response_content = f"""## 📊 查询结果

**需求**: {skill_input}

抱歉，执行查询时出错：{str(sql_err)}

请尝试重新描述你的查询需求。
"""
            
            except Exception as e:
                response_content = f"处理查询时发生错误：{str(e)}"
        else:
            response_content = "请先配置模型引擎才能使用数据问数功能！"
        
        await self.send_response_stream(response_content, conversation_id)
    
    def get_database_schema(self):
        schema_info = []
        with get_connection() as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table['name']
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                col_info = [f"{col['name']} ({col['type']})" for col in columns]
                schema_info.append(f"{table_name}: {', '.join(col_info)}")
        
        return '\n'.join(schema_info)
    
    async def handle_skill_stat(self, skill_input, conversation_id, model_engine):
        if not skill_input:
            response_content = """## 📈 数据统计技能

使用格式：`/stat 统计维度`

示例：
- `/stat 本月采集数据总量`
- `/stat 各采集源数据分布`
- `/stat 深度采集完成率`
- `/stat 用户会话统计`

你可以描述你想要的统计维度，我会帮你生成统计报表。
"""
            await self.send_response_stream(response_content, conversation_id)
            return
        
        with get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM scraped_data")
            scraped_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM scraping_sources")
            source_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM deep_scraped_data")
            deep_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM conversations")
            conv_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM model_engines")
            model_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("SELECT COUNT(*) as count FROM scraping_sources WHERE enabled = 1")
            enabled_source_count = cursor.fetchone()["count"]
            
            cursor = conn.execute("""
                SELECT DATE(scraped_at) as date, COUNT(*) as count 
                FROM scraped_data 
                WHERE scraped_at >= DATE('now', '-7 days')
                GROUP BY DATE(scraped_at)
                ORDER BY date
            """)
            recent_stats = [dict(row) for row in cursor.fetchall()]
        
        skill_input_lower = skill_input.lower()
        
        response_content = f"""## 📈 数据统计报告

**统计维度**: {skill_input}

### 系统数据概览

| 指标 | 数值 |
| --- | --- |
| 采集数据总量 | {scraped_count} 条 |
| 深度分析数据 | {deep_count} 条 |
| 采集源数量 | {source_count} 个 |
| 启用采集源 | {enabled_source_count} 个 |
| 会话总数 | {conv_count} 条 |
| 注册用户 | {user_count} 人 |
| 配置模型 | {model_count} 个 |

"""
        
        if "采集" in skill_input or "scrap" in skill_input_lower:
            response_content += f"""### 采集数据趋势（最近7天）

| 日期 | 采集数量 |
| --- | --- |
"""
            for stat in recent_stats:
                response_content += f"| {stat['date']} | {stat['count']} 条 |\n"
        
        if "完成率" in skill_input or "深度" in skill_input:
            completion_rate = (deep_count / scraped_count * 100) if scraped_count > 0 else 0
            response_content += f"""### 深度采集完成率

- 深度采集完成率：*{completion_rate:.1f}%*
- 已采集：{scraped_count} 条
- 已深度分析：{deep_count} 条
"""
        
        response_content += """
---
*💡 如需更详细的统计，请使用 `/sql` 进行自定义查询*
"""
        
        await self.send_response_stream(response_content, conversation_id)
    
    async def handle_skill_help(self, skill_input, conversation_id, model_engine):
        skills_info = SkillRepository.get_enabled()
        
        response_content = """## 🆘 帮助指引

欢迎使用技能调度系统！以下是当前可用的技能列表：

### 技能列表

"""
        
        for skill in skills_info:
            identifier = skill['skill_identifier']
            name = skill['name']
            desc = skill['description'] or '暂无描述'
            skill_type = '系统' if skill['skill_type'] == 'system' else '自定义'
            
            response_content += f"""#### /{identifier} - {name}

- **类型**: {skill_type}
- **描述**: {desc}

"""
        
        response_content += """### 使用示例

- `/search Python教程` - 搜索相关内容
- `/sql 最近采集的数据` - 查询数据库
- `/stat 采集数据统计` - 查看统计数据
- `/model deepseek-r1` - 切换AI模型
- `/help` - 查看本帮助

### 🎯 提示

直接输入技能指令即可触发对应功能，例如：`/search 天气`
"""
        
        await self.send_response_stream(response_content, conversation_id)
    
    async def handle_skill_model(self, skill_input, conversation_id, model_engine):
        print(f"\n=== 处理模型技能 ===")
        print(f"skill_input: {skill_input}")
        print(f"conversation_id: {conversation_id}")
        if not skill_input:
            models = ModelEngineRepository.get_all(1, 100)
            print(f"获取到的模型列表: {models}")
            
            if not models:
                response_content = """## 🤖 模型切换

当前没有可用的模型引擎。

请在后台管理中添加模型引擎后再试。
"""
            else:
                response_content = """## 🤖 模型切换

请使用 `/model 模型名称` 切换当前会话使用的模型。

**可用模型列表**：

"""
                for model in models:
                    is_default = "（默认）" if model['is_default'] == 1 else ""
                    is_enabled = "启用" if model.get('enabled', 1) == 1 else "禁用"
                    response_content += f"- **{model['name']}** {is_default} - {model['model_name']} ({is_enabled})\n"
                
                response_content += """
**示例**：
- `/model deepseek-r1`
- `/model gpt-4`

*注意：切换模型仅对当前会话有效，刷新页面后将重置为默认模型*
"""
            
            await self.send_response_stream(response_content, conversation_id)
            return
        
        models = ModelEngineRepository.get_all(1, 100)
        target_model = None
        
        skill_input_lower = skill_input.lower()
        for model in models:
            if (model['name'].lower() == skill_input_lower or 
                model['model_name'].lower() == skill_input_lower or
                skill_input_lower in model['name'].lower() or
                skill_input_lower in model['model_name'].lower()):
                target_model = model
                break
        
        if target_model:
            if target_model.get('enabled', 1) != 1:
                response_content = f"""## 🤖 模型切换

抱歉，模型「{target_model['name']}」当前已被禁用，无法切换。

请选择其他可用模型。
"""
            else:
                # 发送模型切换信号给前端
                self.write(f"data: {json.dumps({'model_id': target_model['id'], 'model_name': target_model['name']})}\n\n")
                self.flush()
                
                response_content = f"""## 🤖 模型切换成功

已切换到：**{target_model['name']}**

- 模型标识：{target_model['model_name']}
- 模型类型：{target_model.get('model_type', 'text')}
- 状态：✅ 启用

后续对话将使用此模型进行响应。
"""
        else:
            response_content = f"""## 🤖 模型切换

未找到名为「{skill_input}」的模型。

**可用模型**：
"""
            for model in models:
                if model.get('enabled', 1) == 1:
                    response_content += f"- {model['name']} ({model['model_name']})\n"
            
            response_content += """
请使用 `/model 模型名称` 选择一个可用的模型。
"""
        
        await self.send_response_stream(response_content, conversation_id)
