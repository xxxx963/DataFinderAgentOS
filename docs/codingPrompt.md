任务1：进一步学习并理解项目，将以下信息补全到#basePrompt.md中
1.项目名称：智能数据瞭望与智能问数系统
2.项目背景：通过B/S技术实现一款智能数据采集到深度采集再到数据分析与问数的综合业务系统，以大模型驱动整个业务系统的运行。是一款轻量级的智能（体）应用。
3.技术栈：Python3(python -m venv venv)+sqlite3+websocket+sse+tornado+tornadoTemplate

任务2：进一步学习并理解项目，将以下信息补充到#basePrompt.md中：
1.dist目录下，放置了三个组，用于后台管理侧开发使用其：
-zui-3.0.0.zip:ZUI3 是一个的开源 UI组件库，提供了大量实用组件，支持最大限度的定制，不依赖任何其他JS 框架，可以在任何 Web 应用中通过原生的方式使用。 (开发帮助:https://openzui.com/guide/start/intro.html 组件库帮助：https://openzui.com/lib/basic/core/css-component.html),需要解压再app/static目录下.
-bootstrap-5.3.8-dist.zip :Bootstrap 5.3.8 是一个基于 Bootstrap 5.3.8 版本的 UI 组件，提供了大量实用组件，支持最大限度的定制，不依赖任何其他 JS 框架，可以在任何 Web应用中通过原生的方式使用.(开发帮助:https://getbootstrap.com/docs/5.3/getting-started/introduction/),需解压app/static目录下
-fontawesome-free-6.4.0-web.zip : FontAwesome Awesome 6.4.0 E-个基于 FontAwesome Awesome6.4.0版木的图标库，提供了大量图标，支持自定义图标，可以在任何Web应用中通过原生的方式使用。(开发帮助:https://fontawesome.com/docs/v6.4.0/getting-started/using-free),需解压在app/static目录下

任务3:进一步学习并理解项目，将以下信息补充到#basePrompt.md中:
1、设计风格:自适应浏览器用户区设计、响应式布局、沉浸式操作。
2、所有开发将基于上下文工程提示完成，所有操作需要同步记录和维护以下几个文件:
    -docs/basePrompt.md(项目基提示，AI维护)
    -docs/codingPrompt.md(项目编码提示，人类维护，你不用干预)
    -docs/requirementPrompt.md(项目需求提示，AI维护)

任务4:开始编码实现业务功能模块:
1、完成后台-管理侧功能模块的开发:
-后台登录:采用响应式设计、沉浸式操作、自适应设计，界面风格以企业化管理软件风格为主，简约专业
(后台主要是admin专员使用，默认用户名密码为:admin/admin888)，界而参考上传的UI效果图风格完开发，登录面板需要
居中说屏幕中间位置。
-后台主页:登录后进入后台主页，后期根据需求添加功能模块，本次任务不开发。
-后台管理:采用zui组件实现传统后台管理系统布局:上(L0G0/系统名称/用户信息/)左(莱单区)右(工作区)布局，菜单需要有图标+文字风格设计
2、开发限制:
-严格遵循#basePrompt.md中的设计风格和组件库使用要求。
-所有开发操作需要同步记录和维护以下几个文件:
    -docs/basePrompt.md(项目基础提示，AI维护)
    -docs/codingPrompt.md(项目编码提示，人类维护，你不用维护)
    -docs/requirementPrompt.md(项目需求提示，AI维护)

任务5:开始编码实现业务功能模块:
1、完成后台-管理侧功能模块的开发:
-角色管理:系统分为普通用户、管理用户两大类，普通用户可以通过用户侧测试获得访问前台用户侧的功
有权限。管理用户可以通通后台添加用户获得管理侧权限，管理用户类默认超级管理员(admin)，该角色不允许删除和修改，
可以新增角色/删除/查看/修改/分页(20条/页)/搜索(模糊查询)，需要联动功能，实现角色动态设置功能（二级联动的方式实现）
-用户管理：实现用户新增/删除（admin不允许删除）/修改/查看/分页/搜索
-功能管理：将菜单功能管理化，实现功能的新增/删除/修改/查看/分页/搜索
2、开发限制:
-严格遵循#basePrompt.md中的设计风格和组件库使用要求。
-确保所有的页面的布局、样式、交互等符合设计风格且统一规范一致
-所有开发操作需要同步记录和维护以下几个文件,维护更新为每个大任务完成后，新的大任务开发前更新维护:
    -docs/basePrompt.md(项目基础提示，AI维护)
    -docs/codingPrompt.md(项目编码提示，人类维护，你不用维护)
    -docs/requirementPrompt.md(项目需求提示，AI维护)

任务5.1：发现问题，检查代码，修复问题：
-发现除功能管理有页面外，用户管理和角色管理，点开报错以下的内容，其他的页面都无法点开查看具体的内容，
-需要检查是否正确，是否与项目目录结构一致，同时检查Tornado模板渲染问题。


任务6:开始编码实现业务功能模块:
1、完成后台-管理侧功能横块的开发
-模型引擎:
--实现以橱窗列表展示以及独立的页面风格，页面风格以大模型科技感，炫酷风格为主，区别现在的ZUI风格
--实现动态新增/删除/修改/查询模型引擎。
--支持可视化配置满足OPENAI-API范式的模型服国配置与调用。
--支持统计Token(可视化)
--支持分页-行/三列。6条/页
--支持对模型进行单独的对话测试。
--支持设置模型：默认/模型类型（文字/多模态/视觉/向量）/模型参数（如温度、最大长度等）/系统提示（system_prompt）
--支持SSE流式响应（开关化），支持模型Think开关化
--如要设置为默认模型，系统后续调用模型服务时，优先调用默认模型
以下为openai代码示例:
'''
from openai import OpenAI
client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://aigc-api.aitoolcore.com/api/v1"
)
response = client.chat.completions.create(
    model="deepseek-r1",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
'''
3、开发限制:
-严格遵循#basePrompt.md中的设计风格和组件库使用要求。
-确保所有的页面的布局、样式、交互等符合设计风格且统一规范一致
-所有开发操作需要同步记录和维护以下几个文件,维护更新为每个大任务完成后，新的大人物开发前更新维护:
    -docs/basePrompt.md(项目基础提示，AI维护)
    -docs/codingPrompt.md(项目编码提示，人类维护，你不用维护)
    -docs/requirementPrompt.md(项目需求提示，AI维护)

任务6.1：发现问题，检查代码，修复问题：
-发现模型引擎中，点击模型引擎没有反应，没有内容显示

任务7：开始编码实现业务功能模块：
1.完成后台-管理侧功能模块的开发：
-瞭望采集：通过大模型+AI实现智能数据采集，支持新增瞭望数据源管理及采集功能，以下为具体要求：
--瞭望源管理：一个可动态可视化管理采集规则的功能模块，支持新增/删除/修改/查看/查询等操作，该功能模块可以管理：采集URL，采集URL对对应的RequestHeader等信息，我将给你提供一个采集源的包数据，供你分析实现该管理功能，以下为百度新闻的请求URL和Request Headers包：
RequestHeaders的包数据（原始）:
'''
GET /s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E8%A5%BF%E5%8D%8E%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6&x_bfe_rqs=03E80000000000000000080000000000000000000000000000000000000000000002&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&pn=10 HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: no-cache
Connection: keep-alive
Cookie: BAIDUID_BFESS=10D6E612D9949B30D45D84523D682CD4:FG=1; __bid_n=19cf1e6a92e43689298106; BDUSS=2NtUE9nOHdWZlFaaGxXTzl-UlF0amVOMWN6RTB1bWZOVnpQVDdLVC1NeURvRlZxSVFBQUFBJCQAAAAAAQAAAAEAAADCTX-DbGVlc2hpbmVfYW5nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIMTLmqDEy5qR; BDUSS_BFESS=2NtUE9nOHdWZlFaaGxXTzl-UlF0amVOMWN6RTB1bWZOVnpQVDdLVC1NeURvRlZxSVFBQUFBJCQAAAAAAQAAAAEAAADCTX-DbGVlc2hpbmVfYW5nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIMTLmqDEy5qR; PSTM=1781678669; BD_UPN=12314753; BIDUPSID=634A2076EE4B4A9EF6E9CFD3AA52216E; BA_HECTOR=ak05ak212l2584812k2kagah8424a51l34gin28; H_WISE_SIDS=63141_67861_68165_69004_69294_70116_70123_70627_70803_70549_70848_70909_70938_70968_71031_71039_71049_71057_71068_71079_71095_71104_71139; ZFY=F01d2ukf4G6tIPFXcGU:Bs2AZmkEwmkpEIlxSwtof87A:C; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; X-Use-Search-BFF-WWW=1; delPer=0; H_PS_645EC=3f9bOq2cE%2F2oCSSJt%2FaO%2FcjK60y7GXu0x7kBCzggjmYFGdODfh8GegR7daF1Ep38yKLa; PSINO=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=63141_67861_68165_69004_69294_70116_70123_70627_70803_70549_70848_70909_70938_70968_71031_71039_71049_71057_71068_71079_71095_71104_71139; arialoadData=false; BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; BDSVRTM=526
Host: www.baidu.com
Pragma: no-cache
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0
sec-ch-ua: "Microsoft Edge";v="149", "Chromium";v="149", "Not)A;Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
'''
--瞭望采集：
----开发一个类似搜索引擎的界面，主输入框下方提供采集源的动态选择功能（开关模式），该界面要求独立风格不予ZUI风格同步，炫酷，好看，用户交互体验简单，在采集源的选择面板下，提供参考配置面板（一次有效的采集数量和磁数（与URL中的参数同步）），在参数面板的下方，实施呈现采集到列表（采用橱窗模式，1行3列），列表支持多选/全选，最终可以将选中的数据保存到数据库对应表中，为下一步深度采集作数据准备。

任务8：继续编码实现业务功能模块：
1.完成后台-管理侧功能模块的开发：
-数据仓库模块：以列表显示通过瞭望采集到数据，20/页，支持删除/批量删除/查询/AI深度采集（后续单独任务开发实现：AI深度采集分为单挑采集和批量采集两种模式）
2、开发限制:
-严格遵循#basePrompt.md中的设计风格和组件库使用要求。
-确保所有的页面的布局、样式、交互等符合设计风格且统一规范一致
-所有开发操作需要同步记录和维护以下几个文件,维护更新为每个大任务完成后，新的大人物开发前更新维护:
    -docs/basePrompt.md(项目基础提示，AI维护)
    -docs/codingPrompt.md(项目编码提示，人类维护，你不用维护)
    -docs/requirementPrompt.md(项目需求提示，AI维护)


任务9：继续编码实现业务功能模块：
1.完成后台-管理侧功能模块的开发：
-深度采集：通过技术手段对采集到的数据源进行深度解析，并获得详细的内容，同时需要将详细的内容存储到深度采集对应的表中，还需要与数据仓库中的源进行关联，可以在数据仓库中显示是否深度采集，只有采集过的数据，可以查看深度采集到的详细内容。
--深度采集支持单条或多条数据采集，深度采集过程需要有过程提是，需要采集日志，对结果有简单的统计分析。
--深度采集的技术栈：通过模型引擎中的默认大模型服务+crawlai服务
--深度采集完成后，需要在数据仓库列表中标注深度采集状态
2、开发限制:
-严格遵循#basePrompt.md中的设计风格和组件库使用要求。
-确保所有的页面的布局、样式、交互等符合设计风格且统一规范一致
-所有开发操作需要同步记录和维护以下几个文件,维护更新为每个大任务完成后，新的大人物开发前更新维护:
    -docs/basePrompt.md(项目基础提示，AI维护)
    -docs/codingPrompt.md(项目编码提示，人类维护，你不用维护)
    -docs/requirementPrompt.md(项目需求提示，AI维护)

任务10：开始编码实现前台用户功能模块
1.完成前台用户侧功能模块的开发：
-用户登录：手用后端-管理侧登录模块，实现前端用户侧普通用户的登录功能，与管理和用户共用一套健全逻辑，但是需要区分角色（普通用户）
-用户注册：开放允许注册为普通用户
-AI问数：界面风格采用与CHatgpt/豆包风格类似的可以与AI对话界面效果，需要实现以下功能：
--与AI对话：通过AI调用技能工具SQL实现与sqlite库中相关数据表进行数据问数，（如涉及SQL语句，不允许AI显示具体的SQL语句内容）
--需要建立意图识别，分析用户的问题是问数据库中的表数据还是其他的问题（问天气/问音乐等），这里涉及到不同技能工具的调用和调度
--预留@xxx功能与后台数字员工对话的能力（后续单独任务实现）
--响应数据采用流失响应（SSE）
--组测需要实现模型服务切换（模型服务来自后台模型引擎中可用的模型，默认使用默认模型）
--左侧需要实现历史对话记录，点击可以查看和回放即时对话数据
--对话渲染采用markdown格式渲染结果


任务11：技能仓库体系搭建与指令式技能调度功能开发
--1. 完成后台-管理侧功能模块的开发
 1.1 技能仓库管理
- 新增「技能仓库」后台管理菜单，统一管理系统全部可调度技能，支持**新增、删除、修改、查看、分页（20条/页）、模糊搜索**基础操作，严格遵循ZUI后台管理页面规范。
- 技能核心配置字段：
  - 技能标识：唯一指令触发名，对应`/xxx`中的指令前缀（如`search`），全局唯一不可重复
  - 技能名称：技能对外展示的正式名称
  - 技能描述：功能说明、适用场景与使用示例
  - 技能类型：内置系统技能 / 自定义扩展技能
  - 调用方式：本地逻辑执行 / 第三方API对接 / 大模型工具调用
  - 启用状态：开启/关闭，关闭后前台无法触发该技能调度
  - 排序号：控制前台指令联想提示的展示优先级
- 权限约束：系统内置核心技能**禁止删除**，仅支持修改描述、启用状态与排序；自定义技能支持完整CRUD操作。
- 权限联动：对接现有角色二级联动配置体系，支持为不同角色分配可使用的技能范围；无权限的技能前台不展示、无法触发调度。

1.2 技能调度引擎核心逻辑
- 指令识别规则：统一解析对话消息，精准匹配`/技能标识 触发内容`格式的输入，判定为技能调度指令，**指令调度优先级高于自动意图识别**。
- 调度分发机制：后端搭建统一技能调度入口，根据技能标识路由至对应执行逻辑；执行结果统一接入对话SSE流式输出链路，返回前端渲染展示。
- 异常降级处理：识别到不存在、未启用、无权限的技能时，友好提示对应原因，并返回当前用户可用的技能列表供参考。
- 全链路日志：所有技能调度行为全程记录日志，包含触发用户、技能名称、入参内容、执行结果、耗时，支持后台排查与调用统计。
2. 内置基础调度技能实现
在技能仓库中预置5类核心调度技能，开箱可用：
2.1 网络搜索技能：`/search 关键词`
- 功能：调度全网搜索能力，获取关键词对应的实时网页资讯、公开信息，经大模型整理归纳后返回结构化结果。
- 适用场景：查询时效性新闻、外部行业数据、公共常识等系统本地库外的信息。
2.2 数据问数技能：`/sql 查询需求`
- 功能：将原有AI问数SQL能力纳入技能仓库统一管理，调用大模型生成SQL并执行SQLite业务库查询，返回结构化查询结果，**全程不向用户暴露原始SQL语句**。
- 适用场景：精准查询系统内采集数据、用户数据、运营统计等内部业务数据。
2.3 数据统计技能：`/stat 统计维度`
- 功能：针对系统内数据仓库、采集任务、模型调用等业务数据，生成指定维度的统计分析结果，支持总量统计、趋势分析、占比统计等。
- 指令示例：`/stat 本月瞭望采集数据总量`
2.4 帮助指引技能：`/help`
- 功能：无额外入参，触发后返回当前用户可用的全部技能列表，包含指令格式、功能说明与使用示例，引导用户快速上手技能调度能力。
2.5 模型切换技能：`/model 模型名称`
- 功能：对话过程中通过指令快速切换当前会话使用的大模型，无需手动操作下拉选择框；切换后当前对话后续请求立即生效。
- 指令示例：`/model deepseek-r1`
3. 前台AI问数页面适配开发
- 指令联想交互：用户在输入框输入`/`时，自动弹出可用技能下拉联想框，展示技能标识、名称与简短描述；支持键盘上下键选择、回车自动补全指令。
- 调度状态反馈：触发技能调度后，对话界面展示「正在调用XX技能...」专属加载状态，与普通对话加载态区分，提升交互感知。
- 结果统一渲染：所有技能返回结果统一通过Markdown格式渲染，适配文本、列表、统计卡片等不同结果形态，保持对话界面风格一致。
- 历史对话兼容：技能调度的指令输入与结果输出完整存入对话历史，点击历史记录回放时可完整复现技能调用全过程。
4. 开发限制
- 严格遵循#basePrompt.md中的设计风格和组件库使用要求，后台技能仓库管理页统一使用ZUI组件，保持后台管理体系视觉与交互规范统一。
- 确保所有页面的布局、样式、交互等符合设计风格且统一规范一致，技能调度交互无缝融入现有AI问数对话流程，无体验割裂感。
- 所有开发操作需要同步记录和维护以下几个文件，维护更新为每个大任务完成后，新的大任务开发前更新维护：
    - docs/basePrompt.md（项目基础提示，AI维护）
    - docs/codingPrompt.md（项目编码提示，人类维护，你不用维护）
    - docs/requirementPrompt.md（项目需求提示，AI维护）
