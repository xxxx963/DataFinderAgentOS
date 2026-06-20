# 项目需求文档
*前端侧：面向普通用户，可以通过AI对话实现与数据化员工的交互体验
  *数据库问数
  *天气的问数
  *音乐的问数
  *电影的问数
*后台侧：
  *用户管理
  *角色管理
  *功能管理（联动菜单）
  *模型引擎
  *技能仓库
  *数字员工
  *瞭望采集
  *数据仓库
  *深度采集
  *智能大屏
  *数字孪生
  *普通大屏

## 项目概述
- **项目名称**：智能数据瞭望与智能问数系统
- **项目类型**：轻量级智能（体）应用
- **技术栈**：Python3 + SQLite3 + WebSocket + SSE + Tornado + Tornado模板

## 项目背景
通过B/S技术实现一款智能数据采集到深度采集再到数据分析与问数的综合业务系统，以大模型驱动整个业务系统的运行。

## 设计风格
- 自适应浏览器用户区设计
- 响应式布局
- 沉浸式操作

## 当前功能
1. 用户认证（登录、登出）
2. 基础页面框架
3. 后台登录页面（响应式、企业风格）
4. 后台管理布局（上-左-右结构）

## 待开发功能
（待补充具体需求）

---

## 任务4：后台管理系统开发 ✅ 已完成

### 需求描述
完成后台-管理侧功能模块的开发。

### 功能清单 ✅ 已实现

#### 1. 后台登录 ✅
- **设计风格**：响应式设计、沉浸式操作、自适应设计
- **界面风格**：企业化管理软件风格，简约专业
- **目标用户**：admin专员
- **默认账号**：admin / admin888
- **界面要求**：登录面板居中显示在屏幕中间位置
- **实现文件**：`app/templates/admin/login.html`

#### 2. 后台主页 ✅
- 登录后进入后台主页
- 本次任务不开发具体功能模块，仅保留框架
- **实现文件**：`app/templates/admin/layout.html`

#### 3. 后台管理布局 ✅
- **组件库**：采用 Bootstrap + FontAwesome 实现（ZUI准备中）
- **布局结构**：传统后台管理系统布局
  - 顶部：LOGO / 系统名称 / 用户信息 / 退出按钮
  - 左侧：菜单区（图标+文字风格）
  - 右侧：工作区
- **菜单结构**：
  - 系统管理：用户管理、角色管理、功能管理
  - 智能引擎：模型引擎、技能仓库、数字员工
  - 数据采集：瞭望采集、数据仓库、深度采集
  - 可视化：智能大屏、数字孪生、普通大屏
- **实现文件**：`app/templates/admin/layout.html`、`app/static/css/admin.css`

### 新增文件
- `app/controllers/admin.py` - 后台管理控制器
- `app/templates/admin/base.html` - 后台基础模板
- `app/templates/admin/login.html` - 后台登录页面
- `app/templates/admin/layout.html` - 后台管理布局
- `app/static/css/admin.css` - 后台管理样式
- `init_db.py` - 数据库初始化脚本

### 开发限制
- ✅ 严格遵循 basePrompt.md 中的设计风格和组件库使用要求
- ✅ 同步维护相关文档文件（basePrompt.md、requirementPrompt.md）

---

## 系统启动与部署

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

---

## 任务5：角色、用户、功能管理 ✅ 已完成

### 需求描述
完成后台管理侧的角色管理、用户管理、功能管理模块。

### 功能清单 ✅ 已实现

#### 1. 角色管理 ✅
- **角色列表**：分页显示角色列表（20条/页），支持模糊搜索
- **新增角色**：创建新角色，配置角色名称、描述
- **编辑角色**：修改角色信息，分配功能权限
- **删除角色**：删除角色（默认角色禁止删除）
- **权限分配**：通过二级联动方式为角色分配功能权限
- **实现文件**：
  - `app/controllers/admin.py` - RoleListHandler、RoleEditHandler、RoleDeleteHandler
  - `app/templates/admin/roles.html` - 角色列表页面
  - `app/templates/admin/role_edit.html` - 角色编辑页面
  - `app/models/system.py` - RoleRepository

#### 2. 用户管理 ✅
- **用户列表**：分页显示用户列表（20条/页），支持模糊搜索
- **新增用户**：创建新用户，设置用户名、密码、角色
- **编辑用户**：修改用户信息，可选择是否重置密码
- **删除用户**：删除用户（admin用户禁止删除）
- **角色分配**：为用户分配角色
- **实现文件**：
  - `app/controllers/admin.py` - UserListHandler、UserEditHandler、UserDeleteHandler
  - `app/templates/admin/users.html` - 用户列表页面
  - `app/templates/admin/user_edit.html` - 用户编辑页面
  - `app/models/user.py` - UserRepository（已更新）

#### 3. 功能管理 ✅
- **功能列表**：分页显示功能列表（20条/页），支持模糊搜索
- **新增功能**：创建新功能，配置功能名称、图标、路径、父级、排序
- **编辑功能**：修改功能信息
- **删除功能**：删除功能
- **树形结构**：支持二级菜单结构
- **实现文件**：
  - `app/controllers/admin.py` - FunctionListHandler、FunctionEditHandler、FunctionDeleteHandler
  - `app/templates/admin/functions.html` - 功能列表页面
  - `app/templates/admin/function_edit.html` - 功能编辑页面
  - `app/models/system.py` - FunctionRepository

#### 4. 通用功能 ✅
- **公共组件**：
  - `app/templates/admin/header.html` - 顶部导航栏
  - `app/templates/admin/sidebar.html` - 侧边栏菜单
- **样式文件**：`app/static/css/admin.css` - 后台管理页面样式（已更新）
- **数据库**：
  - 表结构：users（添加role_id字段）、roles、functions、role_functions
  - 默认数据：超级管理员角色、普通用户角色、默认功能菜单、admin用户

### 新增/更新文件
- **新增**：
  - `app/models/system.py` - 角色和功能数据模型
  - `app/templates/admin/roles.html` - 角色列表页面
  - `app/templates/admin/role_edit.html` - 角色编辑页面
  - `app/templates/admin/users.html` - 用户列表页面
  - `app/templates/admin/user_edit.html` - 用户编辑页面
  - `app/templates/admin/functions.html` - 功能列表页面
  - `app/templates/admin/function_edit.html` - 功能编辑页面
  - `app/templates/admin/header.html` - 顶部导航栏组件
  - `app/templates/admin/sidebar.html` - 侧边栏菜单组件
- **更新**：
  - `app/models/user.py` - 用户模型，添加角色支持和分页功能
  - `app/models/db.py` - 数据库初始化，添加新表
  - `app/controllers/admin.py` - 后台控制器，添加角色、用户、功能管理
  - `app.py` - 路由配置，添加新的管理路由
  - `app/static/css/admin.css` - 样式文件，添加管理页面样式
  - `init_db.py` - 初始化脚本，添加默认数据

### 开发限制
- ✅ 严格遵循basePrompt.md中的设计风格和组件库使用要求
- ✅ 确保所有页面的布局、样式、交互符合设计风格且统一规范一致
- ✅ 所有开发操作同步记录和维护相关文档文件

---

## 任务6：模型引擎开发 ✅ 已完成

### 需求描述
完成后台管理侧的模型引擎功能模块开发。

### 功能清单 ✅ 已实现

#### 1. 模型引擎列表 ✅
- **橱窗式展示**：三列网格布局，6条/页分页显示
- **科技感设计**：采用炫酷的科技感UI风格，区别于ZUI风格
- **搜索功能**：支持按模型名称或模型标识模糊搜索
- **Token统计**：可视化展示Token使用统计
- **快速操作**：编辑、测试、设为默认、删除
- **实现文件**：
  - `app/templates/admin/model_engines.html` - 模型引擎列表页面
  - `app/controllers/admin.py` - ModelEngineListHandler

#### 2. 模型引擎编辑 ✅
- **新增/编辑**：支持创建新模型和修改已有模型
- **基本配置**：
  - 模型名称（自定义显示名称）
  - 模型标识（实际API中的model参数）
  - API Key（认证密钥）
  - Base URL（API端点地址）
- **模型类型**：文字、多模态、视觉、向量四种类型
- **参数配置**：
  - Temperature（温度参数）
  - Max Tokens（最大输出Token数）
  - Top P（核采样参数）
  - System Prompt（系统提示词）
- **高级开关**：
  - 设为默认模型
  - 启用SSE流式响应
  - 启用Think模式
- **实现文件**：
  - `app/templates/admin/model_engine_edit.html` - 模型引擎编辑页面
  - `app/controllers/admin.py` - ModelEngineEditHandler

#### 3. 模型对话测试 ✅
- **对话界面**：仿ChatGPT的聊天界面
- **SSE流式输出**：支持Server-Sent Events流式响应（如果启用）
- **消息历史**：显示完整对话历史
- **打字指示器**：AI回复时的打字动画效果
- **实现文件**：
  - `app/templates/admin/model_engine_chat.html` - 模型对话测试页面
  - `app/controllers/admin.py` - ModelEngineChatHandler

#### 4. 模型引擎删除 ✅
- **安全删除**：带确认对话框的删除功能
- **实现文件**：
  - `app/controllers/admin.py` - ModelEngineDeleteHandler

#### 5. 设为默认模型 ✅
- **一键设置**：快速设置模型为默认
- **优先级管理**：系统调用时优先使用默认模型
- **实现文件**：
  - `app/controllers/admin.py` - ModelEngineSetDefaultHandler

#### 6. 数据模型层 ✅
- **数据库表**：`model_engines`表，包含所有模型配置字段
- **仓储类**：`ModelEngineRepository`，提供完整的CRUD操作
- **实现文件**：
  - `app/models/db.py` - 添加 model_engines 表初始化
  - `app/models/system.py` - ModelEngineRepository

### 新增/更新文件
- **新增**：
  - `app/templates/admin/model_engines.html` - 模型引擎列表页面（炫酷科技风）
  - `app/templates/admin/model_engine_edit.html` - 模型引擎编辑页面
  - `app/templates/admin/model_engine_chat.html` - 模型对话测试页面
  - `requirements.txt` - 项目依赖文件（包含 tornado、openai）
- **更新**：
  - `app/models/db.py` - 添加 model_engines 表结构
  - `app/models/system.py` - 添加 ModelEngineRepository
  - `app/controllers/admin.py` - 添加模型引擎相关处理器
  - `app.py` - 添加模型引擎路由
  - `init_db.py` - 初始化默认功能菜单（添加模型引擎菜单项）

### 技术特性
- ✅ 使用 OpenAI SDK 进行 API 调用
- ✅ 支持 SSE 流式响应
- ✅ 完整的错误处理
- ✅ Token 使用量统计和持久化
- ✅ 科技感炫酷UI设计，渐变背景、发光效果、动画过渡
- ✅ 与现有后台架构完全兼容

### 开发限制
- ✅ 严格遵循basePrompt.md中的设计风格和组件库使用要求
- ✅ 确保所有页面的布局、样式、交互符合设计风格且统一规范一致
- ✅ 所有开发操作同步记录和维护相关文档文件

---

## 任务7：前台用户端页面设计 ✅ 已完成

### 需求描述
完成前台用户端页面的美观设计，采用浅紫色、浅粉色和浅蓝色的配色方案，提供舒适的视觉体验。

### 设计风格
- **配色方案**：浅紫粉蓝渐变配色
  - 主色调：柔和紫 (#A78BFA)、柔和粉 (#F472B6)、柔和蓝 (#60A5FA)
  - 背景色：浅紫背景 (#F5F3FF)、浅粉背景 (#FDF2F8)、浅蓝背景 (#EFF6FF)
  - 渐变背景：从浅紫到浅蓝到浅粉的柔和过渡
- **设计理念**：简约、清新、现代、舒适
- **目标用户**：普通用户，面向AI对话交互体验
- **响应式设计**：适配桌面端和移动端

### 功能清单 ✅ 已实现

#### 1. 用户登录页面 ✅
- **设计特点**：
  - 渐变背景动画，柔和流动效果
  - 居中卡片设计，顶部彩色装饰条
  - 圆角Logo图标，渐变背景
  - 柔和的输入框样式，浅紫色背景
  - 渐变登录按钮，悬停浮动效果
- **实现文件**：`app/templates/web/login.html`

#### 2. 用户注册页面 ✅
- **设计特点**：
  - 与登录页面保持一致的设计风格
  - 居中卡片布局
  - 用户名、密码、确认密码三个输入字段
  - 渐变注册按钮
  - 底部链接返回登录页
- **实现文件**：`app/templates/web/register.html`

#### 3. 用户聊天界面 ✅
- **设计特点**：
  - 左侧侧边栏：浅紫到浅蓝渐变背景
    - 新对话按钮，渐变紫色
    - 对话列表，卡片式设计
    - 用户信息区域，头像和退出按钮
  - 右侧主聊天区：
    - 顶部导航栏，模型选择下拉框
    - 消息区域，浅紫渐变背景
    - 欢迎卡片，四个快捷功能入口
    - 消息气泡，用户消息紫粉渐变，AI消息白色卡片
    - 输入区域，圆角输入框，渐变发送按钮
  - 响应式设计：移动端侧边栏可折叠
- **实现文件**：`app/templates/web/chat.html`

#### 4. 统一样式文件 ✅
- **样式内容**：
  - CSS变量定义，统一配色方案
  - 认证页面样式（登录/注册）
  - 聊天界面完整样式
  - 动画效果（渐变流动、打字指示器、悬停效果）
  - 响应式媒体查询
  - Markdown内容渲染样式
- **实现文件**：`app/static/css/user-style.css`

### 新增/更新文件
- **新增**：
  - `app/static/css/user-style.css` - 前台用户端统一样式
- **更新**：
  - `app/templates/web/login.html` - 用户登录页面
  - `app/templates/web/register.html` - 用户注册页面
  - `app/templates/web/chat.html` - 用户聊天界面
  - `docs/requirementPrompt.md` - 需求文档更新

### 设计特性
- ✅ 浅紫粉蓝柔和配色，舒适的视觉体验
- ✅ 渐变背景动画，增加页面活力
- ✅ 圆角卡片设计，现代简约风格
- ✅ 悬停动画效果，提升交互体验
- ✅ 响应式布局，适配多端设备
- ✅ 打字指示器动画，AI回复等待提示
- ✅ Markdown渲染支持，代码块高亮显示
- ✅ 与后台管理系统风格区分，面向不同用户群体

### 开发限制
- ✅ 严格遵循设计风格要求
- ✅ 确保所有页面样式统一规范
- ✅ 同步维护相关文档文件
