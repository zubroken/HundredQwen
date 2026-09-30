# 百问即查（HundredQwen）

一个本地运行的 AI 个性化学习辅助系统，面向大学生提供学生画像构建、个性化智能问答、练习题生成、知识库检索（RAG）和 PPT 自动生成等能力。

- 后端：FastAPI（Python 3，3.12 测试通过）
- 前端：内嵌在后端返回的单页应用（SPA），无独立前端工程
- 模型：默认 DeepSeek，可切换讯飞星火（Spark）
- 数据：SQLite + JSON + 本地知识库文件

> 当前项目以本地测试和功能验证为主，前后端耦合较重，不按生产安全标准设计。

---

## 核心功能

| 模块 | 说明 |
|------|------|
| 账号与学生画像 | 登录、注册、画像读写、注销；内置测试账号 `stu_001` |
| 对话式画像构建 | 通过对话自动生成/增量更新学生画像（`POST /api/chat`） |
| 个性化智能问答 | 基于画像调整回答方式，结合本地知识库做 RAG，带聊天历史上下文（`POST /api/chat-simple`） |
| 练习题生成 | 根据画像与知识库生成针对性题目，返回题目、总分、预计耗时（`POST /api/exercise/generate`） |
| 学习资源与路径 | 读取学生已有学习资源与学习路径 |
| 知识库管理 | 文档导入、分块、关键词检索、统计、导出 `.docx`，可选联动 arXiv 论文 |
| PPT 生成 | 对接讯飞智文：主题列表、任务创建、进度查询，支持 `brief / standard / detailed` 详略控制 |
| LLM 热切换 | `PUT /api/config/llm` 运行时更新当前 LLM 配置 |
| 其他 | 讯飞星火语音识别（ASR）、技能树、每日学习时长追踪 |

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example`（如存在）或设置以下环境变量，`DEEPSEEK_API_KEY` 为必填：

| 变量 | 说明 | 必填 |
|------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API Key | ✅ |
| `DEEPSEEK_BASE_URL` | DeepSeek Base URL | |
| `SPARK_MODEL` / `SPARK_API_KEY` / `SPARK_API_SECRET` / `SPARK_APP_ID` | 讯飞星火配置 | |
| `ZHIWEN_APP_ID` / `ZHIWEN_APP_SECRET` | 讯飞智文 PPT 配置 | |

### 3. 启动服务

默认启动（固定本地地址）：

```bash
python main.py
```

显式指定模型与端口：

```bash
python main.py --model deepseek-chat --host 127.0.0.1 --port 9010
```

Windows 下也可直接使用启动脚本（会复用 9010 端口上已有的服务）：

```powershell
.\start.ps1
```

启动后访问：**http://127.0.0.1:9010**

> Windows 端口冲突时，可先执行 `taskkill /f /im python.exe` 释放端口。

### 4. 重启规则

修改 Python 后端、路由、服务层或页面内嵌 HTML 后，需要重启服务才会加载新代码。

---

## 项目结构

```
HundredQwen/
├── main.py                     # 入口：解析 CLI 参数，启动 uvicorn
├── settings.py                 # 项目根路径、版本号等全局常量
├── requirements.txt            # Python 依赖
├── .env                        # API Key 等环境变量（不提交）
├── api/                        # ────── 路由层 ──────
│   ├── routes.py               #   FastAPI 工厂函数 create_app()
│   ├── home_routes.py          #   GET / 首页
│   ├── home_page.py            #   内嵌 SPA 前端 HTML
│   ├── account_routes.py       #   登录/注册/画像读写/注销
│   ├── learning_routes.py      #   核心学习 API（问答/资源/路径）
│   ├── knowledge_routes.py     #   知识库搜索、导出、统计
│   ├── ppt_routes.py           #   讯飞智文 PPT 创建/进度查询
│   ├── config_routes.py        #   LLM 热切换
│   ├── skill_tree_routes.py    #   技能树 API
│   └── schemas.py              #   所有请求/响应 Pydantic 模型
├── services/                   # ────── 服务层 ──────
│   ├── app_services.py         #   依赖装配中心：build_app_services()
│   ├── llm_service.py          #   DeepSeek LLM 客户端（OpenAI 兼容）
│   ├── spark_service.py        #   讯飞星火 LLM 客户端
│   ├── model_gateway.py        #   多模型网关（deepseek/spark 路由）
│   ├── speech_service.py       #   讯飞星火语音识别（ASR）
│   ├── zhiwen_service.py       #   讯飞智文 PPT API
│   ├── database.py             #   SQLite 数据库管理
│   ├── account_service.py      #   账号注册与画像更新
│   ├── chat_service.py         #   智能问答主编排（RAG + 画像）
│   ├── chat_prompt_service.py  #   RAG 上下文检索 + prompt 组装
│   ├── chat_history_service.py #   聊天历史持久化（JSON）
│   ├── exercise_service.py     #   练习题生成
│   ├── resource_service.py     #   学习资源与路径查询
│   ├── knowledge_base.py       #   本地知识库引擎（分块/索引/检索）
│   ├── knowledge_service.py    #   知识库业务逻辑
│   ├── paper_fetcher.py        #   arXiv 论文抓取
│   ├── docx_exporter.py        #   检索结果导出 .docx
│   ├── ppt_service.py          #   PPT 模板与任务管理
│   ├── skill_tree_service.py   #   技能树服务
│   └── study_time_service.py   #   每日学习时长追踪
├── agents/                     # ────── 智能体层 ──────
│   ├── base_agent.py           #   Agent 基类（LLM 调用 + JSON 解析）
│   ├── orchestrator.py         #   多 Agent 编排器
│   ├── profile_agent.py        #   学生画像构建 Agent
│   ├── document_agent.py       #   学习文档生成 Agent
│   ├── mindmap_agent.py        #   思维导图生成 Agent
│   ├── exercise_agent.py       #   练习题生成 Agent
│   ├── reading_agent.py        #   阅读推荐 Agent
│   ├── code_example_agent.py   #   代码示例生成 Agent
│   └── learning_path_agent.py  #   学习路径规划 Agent
├── models/                     # ────── 数据模型层 ──────
│   ├── profile.py              #   学生画像 Pydantic 模型
│   └── resources.py            #   学习资源 JSON 存储
├── utils/
│   └── helpers.py              #   ID 生成、时间格式化、safe_json_parse
├── data/                       # ────── 数据存储 ──────
│   ├── app.db                  #   SQLite 主库（账号/画像）
│   ├── resources.json          #   学习资源缓存
│   ├── chat_history/           #   聊天记录（按学生 ID 分文件）
│   └── knowledge/              #   本地知识库
└── tests/                      # ────── 测试层 ──────
    ├── test_*_agent.py         #   各 Agent 单元测试
    ├── test_*_service.py       #   各 Service 单元测试
    └── test_routes_integration.py  # 集成测试
```

---

## 主要 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 内嵌 SPA 前端 |
| POST | `/api/login` | 登录 `{student_id, password}` |
| POST | `/api/register` | 注册测试账号 `{nickname}` |
| PUT | `/api/profile/update` | 更新画像 `{student_id, updates}` |
| DELETE | `/api/account/{student_id}` | 注销账号 |
| POST | `/api/chat` | 对话式画像构建 `{student_id?, message, course_name}` |
| POST | `/api/chat-simple` | 个性化问答 `{student_id, message}` |
| POST | `/api/exercise/generate` | 生成练习题 `{student_id, question_type, count, course_name}` |
| GET | `/api/profile/{student_id}` | 获取学生画像 |
| GET | `/api/resources/{student_id}` | 获取学习资源 |
| GET | `/api/paths/{student_id}` | 获取学习路径 |
| PUT | `/api/config/llm` | 热更新 LLM 配置 |
| GET | `/api/knowledge/documents` | 知识库文档列表 |
| POST | `/api/knowledge/search` | 搜索知识库 `{query, type_filter, doc_id, include_arxiv}` |
| POST | `/api/knowledge/export` | 导出检索结果到 docx |
| GET | `/api/knowledge/stats` | 知识库统计 |
| GET | `/api/zhiwen/themes` | PPT 模板列表 |
| POST | `/api/zhiwen/ppt/create` | 创建 PPT 任务 `{query, theme, detail_level}` |
| POST | `/api/zhiwen/ppt/progress` | 查询 PPT 进度 `{sid}` |

---

## 数据存储

| 内容 | 位置 |
|------|------|
| 学生账号与画像 | `data/app.db`（SQLite） |
| 聊天历史 | `data/chat_history/`（按学生 ID 分 JSON 文件） |
| 学习资源缓存 | `data/resources.json` |
| 本地知识库 | `data/knowledge/`（分块 chunks + 目录 toc） |

---

## 测试与验证

```powershell
python check_server.py
Invoke-WebRequest http://127.0.0.1:9010/api/knowledge/stats
Invoke-WebRequest http://127.0.0.1:9010/api/generation/resource-bundles/stu_001
```

单元与集成测试位于 `tests/` 目录。

## 无模型降级

真实模型不可用时，资源生成服务会使用本地知识库 chunk 构造 fallback 资源，保留引用和 warning，不伪造来源。

---

## 文档

- [项目功能总览](项目功能总览.md)
- [项目架构文档](项目架构文档.md)
- [部署运行说明](docs/部署运行说明.md)
- [需求分析说明书](docs/需求分析说明书.md)
- [系统开发说明书](docs/系统开发说明书.md)
- [测试说明书](docs/测试说明书.md)
