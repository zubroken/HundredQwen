# 固定端口与无缓存启动设计

## 目标

让 HundredQwen 始终使用 `127.0.0.1:9010`：已有本项目服务时复用，端口被其他程序占用时明确报错，不再因重复启动产生新端口；首页每次重新获取最新 HTML。

## 方案

新增 Windows 启动脚本 `start.ps1`。它先请求 `/api/config/llm/status`：成功即复用已有服务；若 9010 被非本项目进程占用，则输出 PID 并退出；若端口空闲，才启动 `main.py --host 127.0.0.1 --port 9010`。脚本不终止所有 Python 进程。

首页响应增加 `Cache-Control: no-store`，只禁用应用 HTML 的浏览器缓存，不删除 SQLite、聊天历史或知识库分块。聊天历史仍由现有服务持久化，和端口无关。

## 验收

- `start.ps1` 在已有 HundredQwen 服务时不创建第二个 Python 进程。
- 9010 被非 HundredQwen 进程占用时脚本失败且不切换端口。
- 根路径响应包含 `Cache-Control: no-store`。
