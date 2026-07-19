# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## 启动命令

```bash
# 安装依赖
pip install -r requirements.txt

# 默认启动（固定本地地址）
python main.py

# 显式指定模型与端口
python main.py --model deepseek-chat --host 127.0.0.1 --port 9010

# 自定义 API Key
python main.py --api-key sk-xxx --host 127.0.0.1 --port 9010
```

Windows 端口冲突时，可先执行：

```powershell
taskkill /f /im python.exe
```

## 当前结构概览

### 路由层

- 应用入口在 [api/routes.py](/D:/my_codex_project/HundredQwen/api/routes.py)
- `create_app()` 只负责创建 `FastAPI` 应用、构建 `AppServices`、注册路由
- 路由已按领域拆分：
  - [api/home_routes.py](/D:/my_codex_project/HundredQwen/api/home_routes.py)
  - [api/account_routes.py](/D:/my_codex_project/HundredQwen/api/account_routes.py)
  - [api/learning_routes.py](/D:/my_codex_project/HundredQwen/api/learning_routes.py)
  - [api/config_routes.py](/D:/my_codex_project/HundredQwen/api/config_routes.py)
  - [api/ppt_routes.py](/D:/my_codex_project/HundredQwen/api/ppt_routes.py)
  - [api/knowledge_routes.py](/D:/my_codex_project/HundredQwen/api/knowledge_routes.py)
- 请求/响应模型集中在 [api/schemas.py](/D:/my_codex_project/HundredQwen/api/schemas.py)
- 首页仍为内嵌式单页界面，HTML 内容在 [api/home_page.py](/D:/my_codex_project/HundredQwen/api/home_page.py)

### 服务层

- [services/account_service.py](/D:/my_codex_project/HundredQwen/services/account_service.py)：账号、画像读写、画像更新
- [services/chat_service.py](/D:/my_codex_project/HundredQwen/services/chat_service.py)：问答主编排
- [services/chat_history_service.py](/D:/my_codex_project/HundredQwen/services/chat_history_service.py)：聊天历史与上下文
- [services/chat_prompt_service.py](/D:/my_codex_project/HundredQwen/services/chat_prompt_service.py)：RAG 上下文与 system prompt 组装
- [services/exercise_service.py](/D:/my_codex_project/HundredQwen/services/exercise_service.py)：练习题生成
- [services/resource_service.py](/D:/my_codex_project/HundredQwen/services/resource_service.py)：学习资源与学习路径查询
- [services/knowledge_service.py](/D:/my_codex_project/HundredQwen/services/knowledge_service.py)：知识库查询、导出、统计
- [services/ppt_service.py](/D:/my_codex_project/HundredQwen/services/ppt_service.py)：PPT 模板、创建、进度查询
- [services/app_services.py](/D:/my_codex_project/HundredQwen/services/app_services.py)：应用装配与 LLM 热更新编排

### 智能体与遗留结构

- [agents/orchestrator.py](/D:/my_codex_project/HundredQwen/agents/orchestrator.py) 仍保留为历史结构参考
- 旧的“多智能体全资源自动生成”前端入口已经不再是当前主链路
- 当前主链路是：
  - `POST /api/chat`：对话式画像构建
  - `POST /api/chat-simple`：个性化智能问答
  - `POST /api/exercise/generate`：练习题生成
  - `POST /api/knowledge/search`：知识库检索
  - `POST /api/zhiwen/ppt/create`：PPT 生成

## 数据存储

- SQLite：`data/app.db`
- 聊天历史：`data/chat_history/`
- 资源缓存：`data/resources.json`
- 本地知识库：`data/knowledge/`

## LLM 现状

- 默认问答主链路使用 [services/llm_service.py](/D:/my_codex_project/HundredQwen/services/llm_service.py)，当前实际底层是 DeepSeek/OpenAI 兼容调用
- [services/spark_service.py](/D:/my_codex_project/HundredQwen/services/spark_service.py) 已存在，但当前未接入聊天/画像/练习题主业务链路
- [services/zhiwen_service.py](/D:/my_codex_project/HundredQwen/services/zhiwen_service.py) 负责讯飞智文 PPT 能力

## 关键约定

- 项目只用于本地测试，不按生产安全标准设计
- 测试用户：`stu_001`
- 默认本地启动地址：`http://127.0.0.1:9010`
- 当前账号体系为本地测试止血版，不包含正式 token/session 认证流
- `PUT /api/config/llm` 支持运行时热更新当前 LLM 配置

## 当前 API

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
| GET | `/api/knowledge/documents` | 获取知识库文档列表 |
| POST | `/api/knowledge/search` | 搜索知识库 `{query, type_filter, doc_id, include_arxiv}` |
| POST | `/api/knowledge/export` | 导出知识库结果到 docx |
| GET | `/api/knowledge/stats` | 获取知识库统计 |
| GET | `/api/zhiwen/themes` | 获取 PPT 模板列表 |
| POST | `/api/zhiwen/ppt/create` | 创建 PPT 任务 `{query, theme, detail_level}`，兼容旧字段 `page_count` |
| POST | `/api/zhiwen/ppt/progress` | 查询 PPT 进度 `{sid}` |

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API Key | Y |
| `DEEPSEEK_BASE_URL` | DeepSeek Base URL | N |
| `SPARK_MODEL` | Spark 模型名 | N |
| `SPARK_API_KEY` | Spark API Key | N |
| `SPARK_API_SECRET` | Spark API Secret | N |
| `SPARK_APP_ID` | Spark App ID | N |
| `ZHIWEN_APP_ID` | 讯飞智文应用 ID | N |
| `ZHIWEN_APP_SECRET` | 讯飞智文应用 Secret | N |
