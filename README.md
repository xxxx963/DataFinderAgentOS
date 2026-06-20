# 智能数据瞭望系统

一个基于 Tornado 框架的 AI 对话平台，集成多模型引擎管理与数字员工调度能力。

## 功能特性

### 核心功能
- **智能对话** - 支持多模型切换，SSE 流式响应
- **技能系统** - 内置网络搜索、数据问数、统计分析、模型切换等技能
- **数字员工** - 天气助手、音乐助手、西师妹等智能服务
- **管理后台** - 完整的角色权限、用户管理、模型配置、技能编排

### 技能指令
| 指令 | 功能 | 示例 |
|------|------|------|
| `/search` | 网络搜索 | `/search 人工智能发展趋势` |
| `/sql` | 数据问数 | `/sql 查询用户数量` |
| `/stat` | 数据统计 | `/stat 统计本月访问量` |
| `/model` | 模型切换 | `/model GPT-4` |
| `/help` | 帮助指引 | `/help` |

## 技术架构

```
├── app.py                 # 主入口程序
├── app/
│   ├── controllers/       # 控制器层
│   │   ├── chat.py        # 对话处理（SSE流式响应）
│   │   ├── admin.py       # 后台管理
│   │   ├── auth.py        # 用户认证
│   │   └── digital_employee.py  # 数字员工
│   ├── models/            # 数据模型层
│   │   ├── db.py          # 数据库连接
│   │   ├── system.py      # 系统模型（角色、功能、技能）
│   │   └── user.py        # 用户模型
│   ├── static/            # 静态资源
│   │   ├── css/           # 样式文件
│   │   └── fontawesome/   # 图标库
│   └── templates/         # 模板文件
│       ├── admin/         # 后台管理页面
│       └── web/           # 前端用户页面
├── docs/                  # 项目文档
└── database/              # SQLite 数据库
```

## 快速开始

### 环境要求
- Python 3.10+
- Tornado 6.x
- SQLite 3

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量
1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入实际配置：
```
COOKIE_SECRET=your_secure_cookie_secret
XISHIMEI_API_KEY=your_api_key
WEATHER_API_KEY=your_api_key
MUSIC_API_KEY=your_api_key
```

### 启动服务
```bash
python app.py
```

### 访问地址
- 前端聊天页面: http://localhost:10086/home
- 管理员登录页面: http://localhost:10086/admin/login

## RESTful API

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/models` | GET | 获取模型列表 |
| `/api/skills` | GET | 获取技能列表 |
| `/api/employees` | GET | 获取数字员工列表 |
| `/api/conversations` | GET | 获取对话列表 |
| `/api/conversations/{id}` | GET | 获取对话详情 |
| `/api/chat/stream` | GET | 流式对话（SSE） |

## 界面主题

采用浅蓝（#06b6d4）与浅粉（#f472b6）渐变色系，提供清新现代的视觉体验。

## 许可证

MIT License