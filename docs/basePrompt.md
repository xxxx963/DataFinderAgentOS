# 项目信息
1. 项目名称：智能数据瞭望与智能问数系统
2. 项目背景：通过B/S技术实现一款智能数据采集到深度采集再到数据分析与问数的综合业务系统，以大模型驱动整个业务系统的运行。是一款轻量级的智能（体）应用。
3. 技术栈：Python3(python -m venv venv)+sqlite3+websocket+sse+tornado+tornadoTemplate

---

# 项目结构
```
DataFinderAgentOS/
├─app/                          # 应用主目录
│  ├─controllers/               # 控制层目录（MVC模式中的Controller层）
│  │  ├─base.py            # 基类控制器，所有控制器继承此类
│  │  ├─auth.py            # 用户认证相关控制器（登录、登出）
│  │  ├─home.py            # 首页控制器
│  │  ├─admin.py           # 后台管理控制器
│  │  └─__pycache__/
│  ├─models/                  # 模型层目录（MVC模式中的Model层）
│  │  ├─db.py              # 数据库连接和初始化
│  │  ├─user.py            # 用户数据模型和仓储类
│  │  ├─system.py          # 系统管理相关模型（角色、功能、模型引擎）
│  │  └─__pycache__/
│  ├─static/                  # 静态资源目录
│  │  ├─css/                 # CSS样式目录
│  │  │  ├─base.css        # 基础样式
│  │  │  └─admin.css       # 后台管理样式
│  │  ├─js/                  # JS脚本目录
│  │  ├─bootstrap-5.3.8-dist/  # Bootstrap前端框架
│  │  └─fontawesome-free-6.4.0-web/  # FontAwesome图标库
│  ├─templates/               # 视图目录（MVC模式中的View层）
│  │  ├─admin/               # 后台管理页面目录
│  │  │  ├─base.html        # 后台基础模板
│  │  │  ├─login.html       # 后台登录页面
│  │  │  └─layout.html      # 后台管理布局
│  │  └─web/                 # 前台用户侧页面目录
│  │     ├─base.html          # 基础模板
│  │     ├─login.html         # 登录页面
│  │     └─index.html         # 首页
│  └─__pycache__/
├─database/                     # 数据库目录
│  └─app.db                 # SQLite数据库文件
├─dist/                         # 第三方组件库
├─docs/                         # 开发提示词工程目录
├─test/                         # 单元测试脚本目录
├─venv/                         # Python虚拟环境
├─app.py                        # 主入口程序
└─init_db.py                    # 数据库初始化脚本
```

---

# 开发模式与架构设计

## 1. MVC架构模式
项目采用经典的 **MVC（Model-View-Controller）** 架构模式：

- **Model层**：位于 `app/models/`，负责数据存储、业务逻辑和数据库交互
  - `db.py`：提供数据库连接和初始化
  - `user.py`：用户仓储类，管理用户的创建、查询、验证等
  - `system.py`：系统仓储类，包含 RoleRepository、FunctionRepository、ModelEngineRepository
    - `ModelEngineRepository`：管理AI模型引擎的增删改查、设置默认、Token统计等

- **View层**：位于 `app/templates/`，负责页面展示
  - 使用 Tornado 模板引擎
  - 模板继承机制（base.html）
  - 前后台分离的模板目录

- **Controller层**：位于 `app/controllers/`，负责处理请求、调用Model、渲染View
  - `base.py`：基类控制器，统一处理用户认证（get_current_user）
  - 所有控制器继承自 `BaseHandler`
  - 使用 `@tornado.web.authenticated` 装饰器实现认证保护

## 2. 技术实现细节

### 数据库
- 使用 **SQLite3** 作为数据存储
- 数据库文件：`database/app.db`
- 密码加密：PBKDF2-HMAC-SHA256 加盐加密，迭代100,000次
- 使用 `sqlite3.Row` 工厂使查询结果支持字典访问

### 安全特性
- **XSRF保护：`xsrf_cookies=True
- **安全Cookie**：使用 `set_secure_cookie` 和 `get_secure_cookie`
- **用户认证**：基于Cookie的会话管理

### 前端技术
- **Bootstrap 5.3.8**：响应式UI框架
- **FontAwesome 6.4.0**：图标库
- **ZUI 3.0.0**：开源UI组件库（需要从 dist 目录解压到 app/static）
- **Tornado模板**：模板引擎

### 第三方组件库（dist 目录）
dist 目录下存放了三个UI组件库的压缩包，用于后台管理侧开发：

| 组件库 | 说明 | 开发帮助 | 组件库帮助 |
|--------|------|----------|------------|
| `zui-3.0.0.zip` | ZUI3 是一个开源UI组件库，提供了大量实用组件，支持最大限度的定制，不依赖任何其他JS框架，可以在任何Web应用中通过原生的方式使用。 | https://openzui.com/guide/start/intro.html | https://openzui.com/lib/basic/core/css-component.html |
| `bootstrap-5.3.8-dist.zip` | Bootstrap 5.3.8 是一个基于 Bootstrap 5.3.8 版本的 UI 组件，提供了大量实用组件，支持最大限度的定制，不依赖任何其他 JS 框架，可以在任何 Web 应用中通过原生的方式使用。 | https://getbootstrap.com/docs/5.3/getting-started/introduction/ | - |
| `fontawesome-free-6.4.0-web.zip` | FontAwesome 6.4.0 是一个基于 FontAwesome 6.4.0 版本的图标库，提供了大量图标，支持自定义图标，可以在任何 Web 应用中通过原生的方式使用。 | https://fontawesome.com/docs/v6.4.0/getting-started/using-free | - |

**使用说明**：所有组件库需要解压到 `app/static` 目录下使用。

## 3. 路由配置

| 路由 | 方法 | 处理器 | 说明 |
|------|------|--------|------|
| `/` | GET | LoginHandler | 登录页 |
| `/home` | GET | HomeHandler | 首页（需认证） |
| `/user/login` | POST | LoginHandler | 登录提交 |
| `/user/logout` | POST | LogoutHandler | 登出 |
| `/admin/login` | GET/POST | AdminLoginHandler | 后台登录页 |
| `/admin/logout` | POST | AdminLogoutHandler | 后台登出 |
| `/admin` | GET | AdminHomeHandler | 后台管理首页（需认证） |
| `/admin/roles` | GET | RoleListHandler | 角色列表 |
| `/admin/roles/new` | GET/POST | RoleEditHandler | 新增角色 |
| `/admin/roles/{id}` | GET/POST | RoleEditHandler | 编辑角色 |
| `/admin/roles/delete/{id}` | POST | RoleDeleteHandler | 删除角色 |
| `/admin/users` | GET | UserListHandler | 用户列表 |
| `/admin/users/new` | GET/POST | UserEditHandler | 新增用户 |
| `/admin/users/{id}` | GET/POST | UserEditHandler | 编辑用户 |
| `/admin/users/delete/{id}` | POST | UserDeleteHandler | 删除用户 |
| `/admin/functions` | GET | FunctionListHandler | 功能列表 |
| `/admin/functions/new` | GET/POST | FunctionEditHandler | 新增功能 |
| `/admin/functions/{id}` | GET/POST | FunctionEditHandler | 编辑功能 |
| `/admin/functions/delete/{id}` | POST | FunctionDeleteHandler | 删除功能 |
| `/admin/model-engines` | GET | ModelEngineListHandler | 模型引擎列表 |
| `/admin/model-engines/new` | GET/POST | ModelEngineEditHandler | 新增模型引擎 |
| `/admin/model-engines/{id}` | GET/POST | ModelEngineEditHandler | 编辑模型引擎 |
| `/admin/model-engines/delete/{id}` | POST | ModelEngineDeleteHandler | 删除模型引擎 |
| `/admin/model-engines/set-default/{id}` | POST | ModelEngineSetDefaultHandler | 设为默认模型 |
| `/admin/model-engines/chat/{id}` | GET/POST | ModelEngineChatHandler | 模型对话测试 |

## 4. 启动方式

### 环境要求
- Python 3.x
- 虚拟环境已配置（位于 `.venv` 目录）

### Windows 系统启动步骤

```bash
# 1. 激活虚拟环境（如果未激活）
.venv\Scripts\activate

# 2. 初始化数据库并创建默认用户（仅首次运行需要）
.venv\Scripts\python.exe init_db.py

# 3. 启动服务器
.venv\Scripts\python.exe app.py
```

### Linux/Mac 系统启动步骤

```bash
# 1. 激活虚拟环境（如果未激活）
source .venv/bin/activate

# 2. 初始化数据库并创建默认用户（仅首次运行需要）
.venv/bin/python init_db.py

# 3. 启动服务器
.venv/bin/python app.py
```

### 访问地址
- 服务器默认监听端口：**10086**
- 后台管理地址：http://localhost:10086/admin
- 前台地址：http://localhost:10086/

### 默认管理员账号
- 用户名：`admin`
- 密码：`admin888`

### 注意事项
- 确保虚拟环境已正确配置
- 确保端口 10086 未被占用
- 首次运行必须先执行 init_db.py 初始化数据库

## 5. 功能特性

### 后台登录页面
- 响应式设计，自适应各种屏幕尺寸
- 沉浸式操作体验
- 企业化管理软件风格，简约专业
- 登录面板居中显示于屏幕中央
- 渐变背景，卡片式设计
- 图标+文字输入框
- 友好的错误提示

### 后台管理布局
- 传统后台管理系统布局（上-左-右结构）
- 顶部：LOGO、系统名称、用户信息、退出按钮
- 左侧：菜单导航区（图标+文字风格）
- 右侧：工作区
- 使用 Bootstrap 5.3.8 + FontAwesome 6.4.0 构建
- 响应式设计，移动端自动调整侧边栏宽度

### 模型引擎功能
- **橱窗式列表展示**：三列网格布局，6条/页，科技感炫酷设计风格
- **完整CRUD**：支持动态新增/删除/修改/查询模型引擎
- **OpenAI API 兼容**：支持可视化配置兼容 OpenAI API 范式的模型服务
- **Token 统计**：可视化统计模型使用的 Token 数量
- **多种模型类型**：支持文字/多模态/视觉/向量等不同模型类型配置
- **高级参数设置**：支持温度、最大长度、Top P、系统提示词等参数配置
- **SSE 流式响应**：支持开关化的 Server-Sent Events 流式响应
- **Think 模式**：支持模型 Think 模式开关
- **默认模型设置**：可设置默认模型，系统调用时优先使用默认模型
- **对话测试**：支持对每个模型进行单独的对话测试

## 6. 设计风格
- **自适应浏览器用户区设计**
- **响应式布局**
- **沉浸式操作**

## 7. 开发规范
- 所有控制器继承 `BaseHandler`
- 使用 `@tornado.web.authenticated` 装饰需要登录的页面
- 数据库操作使用上下文管理器 (`with get_connection() as conn`)
- 模板继承自 `base.html` 统一页面结构

## 8. 开发工作流

### 上下文工程提示文件
所有开发将基于上下文工程提示完成，所有操作需要同步记录和维护以下几个文件：

| 文件 | 说明 | 维护者 |
|------|------|--------|
| `docs/basePrompt.md` | 项目基提示，包含项目信息、架构、代码规范等 | AI维护 |
| `docs/codingPrompt.md` | 项目编码提示，包含具体开发任务指令 | 人类维护，AI不干预 |
| `docs/requirementPrompt.md` | 项目需求提示，包含需求文档 | AI维护 |

---

# 代码规范

## 9. 命名规范

### 文件和目录
- 目录名：小写，使用下划线分隔（如 `controllers`、`templates`）
- Python 文件名：小写，使用下划线分隔（如 `auth.py`、`user.py`、`admin.py`）
- 模板文件名：小写，使用下划线分隔（如 `login.html`、`layout.html`）

### 类名
- 使用 **PascalCase（大驼峰）** 命名
- 控制器类以 `Handler` 结尾（如 `LoginHandler`、`AdminLoginHandler`）
- 模型类以 `Repository` 结尾（如 `UserRepository`）

### 函数和方法
- 使用 **snake_case（小写下划线）** 命名
- 私有函数/方法以下划线开头（如 `_hash_password`）

### 变量和常量
- 变量名：**snake_case**（如 `username`、`password_hash`）
- 常量：全大写，下划线分隔（如 `DB_PATH`）

## 10. 包和模块规范

### `__init__.py` 文件
每个包目录必须包含 `__init__.py`，并添加说明文档：
```python
"""
包名：[简要说明]
约定：
- [约定1]
- [约定2]
"""
```

### 模块导入
- 标准库导入在前
- 第三方库导入居中
- 本地模块导入在后
- 各组之间空一行

## 11. Controller 层规范

### 文件组织
- **一个业务模块一个文件**（如 `auth.py`、`home.py`、`admin.py`）
- 所有 Handler 继承自 `BaseHandler`

### Handler 职责
- 接收请求、校验参数
- 调用 Model 层处理业务逻辑
- 渲染 View 或返回响应
- **不直接操作数据库**

### 认证保护
- 需要登录的页面使用 `@tornado.web.authenticated` 装饰器
- `login_url` 设置为 `/admin/login`（后台）

## 12. Model 层规范

### 仓储模式
- 使用 **Repository 模式**封装数据访问
- 类名格式：`{实体名}Repository`
- 方法使用 `@staticmethod` 装饰

### 数据库操作
- 使用 `get_connection()` 获取连接
- 使用 **上下文管理器** 管理连接：`with get_connection() as conn:`
- SQL 语句使用参数化查询，防止 SQL 注入
- 错误处理使用 `try-except`

### 密码安全
- 使用 PBKDF2-HMAC-SHA256 加盐加密
- 迭代次数：100,000
- Salt 长度：16 字节（hex 32字符）

## 13. View 层规范

### 模板继承
- 所有页面模板继承自对应的 base.html
- 前台页面在 `web/` 目录下，继承 `base.html`
- 后台页面在 `admin/` 目录下，继承 `base.html`
- 使用 `{% block body %}{% end %}` 定义内容块

### 静态资源
- 使用 `{{ static_url('path/to/resource') }}` 引用静态文件
- CSS 放在 `<head>` 中
- JS 使用 `defer` 属性延迟加载
- 后台使用独立的 `admin.css` 样式文件

### XSRF 保护
- 所有 POST 表单必须包含 `{% module xsrf_form_html() %}`

## 14. 注释规范

### 文件注释
每个 Python 文件开头添加注释说明用途：
```python
# [简要说明文件用途]
```

### 函数/方法注释
复杂函数添加注释说明功能、参数、返回值

### 行内注释
- 使用 `#` 开头
- 与代码保持适当距离
- 解释"为什么"而不是"是什么"

## 15. 安全规范

### Cookie 安全
- 使用 `set_secure_cookie` 和 `get_secure_cookie`
- `cookie_secret` 在生产环境必须修改

### XSRF 保护
- 应用设置 `xsrf_cookies=True`
- 所有 POST 请求必须包含 XSRF token

### 输入验证
- 所有用户输入必须验证
- 使用 `get_body_argument` 或 `get_argument` 获取参数
- 提供默认值防止 KeyError

## 16. 错误处理

### HTTP 状态码
- 400：客户端请求错误（参数缺失）
- 401：未授权（登录失败）
- 403：禁止访问
- 404：未找到
- 500：服务器错误

### 用户反馈
- 错误信息通过 `error` 变量传递给模板
- 友好的错误提示，不暴露技术细节
