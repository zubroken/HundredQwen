# Single-Instance Startup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 固定 HundredQwen 的本地端口并避免浏览器复用旧首页。

**Architecture:** 使用一个可测试的启动决策模块处理端口占用和健康检查；PowerShell 脚本只负责执行该决策。根路由仅增加 HTML 缓存控制头。

**Tech Stack:** Python、FastAPI、PowerShell、unittest。

---

### Task 1: 启动决策逻辑

**Files:**
- Create: `services/startup.py`
- Test: `tests/test_startup.py`

- [ ] 编写失败测试：健康检查成功时返回 `reuse`；端口被其他进程占用时返回 `conflict`；端口空闲时返回 `start`。
- [ ] 实现最小 `decide_start_action` 函数。
- [ ] 运行 `python -m pytest tests/test_startup.py -q`。

### Task 2: 单实例 PowerShell 启动器

**Files:**
- Create: `start.ps1`

- [ ] 使用 9010 健康检查复用已运行应用。
- [ ] 仅当端口空闲时后台启动 `main.py --host 127.0.0.1 --port 9010`。
- [ ] 端口冲突时退出并显示 PID；不结束其他 Python 进程。

### Task 3: 首页缓存控制

**Files:**
- Modify: `api/home_routes.py`
- Modify: `tests/test_home_page.py`

- [ ] 编写失败测试，要求根页面含 `Cache-Control: no-store`。
- [ ] 添加响应头。
- [ ] 运行相关测试及完整测试套件。
