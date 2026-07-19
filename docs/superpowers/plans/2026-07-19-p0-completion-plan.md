# P0 比赛要求闭环实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 HundredQwen 从“多个 Agent 和独立能力并存”推进为可在 7 分钟内稳定演示的“画像 → 多 Agent 资源包 → 个性化路径 → 学习反馈 → 安全引用”的完整主流程，并补齐初赛提交所需的开发、测试、部署和工具说明文档。

**Architecture:** 保留现有 FastAPI + 内嵌 SPA + SQLite/JSON 架构，不重写前端、不引入任务队列。新增一个面向演示的 `ResourceGenerationService` 作为统一业务入口，负责调用现有 Agent、持久化资源和学习路径；新增安全与引用校验层，在模型输出返回前进行敏感词过滤、知识库依据标记和低依据提示。所有耗时生成先采用同步接口，必要时通过前端状态提示和统一错误处理避免白屏；PPT 继续使用现有异步进度接口。

**Tech Stack:** Python 3、FastAPI、Pydantic、SQLite、现有 `ResourceDB` JSON 存储、现有 DeepSeek/Spark 网关、现有 Agent、内嵌 HTML/CSS/JavaScript、pytest。

---

## 一、范围和最终验收场景

最终只承诺一条可稳定演示的主场景，避免把所有历史 Agent 入口同时暴露：

```text
登录 stu_001
  → 查看已有画像
  → 输入“我想系统学习 Transformer 注意力机制”
  → 系统检索教材并显示引用依据
  → Orchestrator 分解任务
  → 文档 / 思维导图 / 练习题 / 拓展阅读 / 代码案例 Agent 协作生成
  → 保存 5 类资源
  → LearningPathAgent 根据资源和画像生成有顺序的学习路径
  → 仪表盘显示资源卡片和路径节点
  → 开始学习、完成一道题、暂停学习
  → 展示本周学习时间和路径进度
```

P0 不包含：正式账号 Token 体系、生产级权限、多租户、前后端拆分、真正的视频生成平台、云端部署。

每个阶段都必须保留一个可运行版本；不得先删除当前问答、练习题、知识库、PPT 和学习计时功能。

## 二、文件地图

### 新建文件

- `HundredQwen/services/resource_generation_service.py`：统一资源包生成、Agent 协作、路径生成和持久化。
- `HundredQwen/services/content_safety_service.py`：输入/输出安全检查、风险等级和拒答信息。
- `HundredQwen/services/citation_service.py`：知识库依据抽取、引用元数据和依据不足标记。
- `HundredQwen/api/generation_routes.py`：资源包生成与路径查询接口，避免继续扩大 `learning_routes.py`。
- `HundredQwen/tests/test_resource_generation_service.py`：Agent 协作、资源持久化和失败回滚测试。
- `HundredQwen/tests/test_generation_routes.py`：接口契约、错误状态和响应结构测试。
- `HundredQwen/tests/test_content_safety_service.py`：敏感输入、敏感输出、正常内容测试。
- `HundredQwen/tests/test_citation_service.py`：有依据、无依据、多条依据测试。
- `HundredQwen/tests/test_generation_flow.py`：使用 Stub Agent 的端到端主流程测试。
- `HundredQwen/docs/需求分析说明书.md`：用户痛点、角色、需求与技术映射。
- `HundredQwen/docs/系统开发说明书.md`：架构、Agent、数据、接口、前端和安全实现。
- `HundredQwen/docs/测试说明书.md`：测试范围、用例、结果、已知限制。
- `HundredQwen/docs/部署运行说明.md`：环境变量、安装、启动、重启、故障排查。
- `HundredQwen/docs/知识库与测试数据说明.md`：课程范围、来源、目录、构造方式和测试账号。
- `HundredQwen/docs/第三方依赖与AI工具说明.md`：开源依赖、协议、来源及 AI Coding 工具使用说明。
- `HundredQwen/docs/演示脚本.md`：7 分钟演示时间轴、操作步骤、备用话术和失败兜底。

### 修改文件

- `HundredQwen/models/resources.py`：补充资源包元数据、引用字段和路径节点的来源关联；保持旧 JSON 可读取。
- `HundredQwen/services/app_services.py`：装配新服务并注入现有 Agent、知识库和 `ResourceDB`。
- `HundredQwen/api/routes.py`：注册 `generation_routes`。
- `HundredQwen/api/schemas.py`：新增生成请求、生成响应、路径状态模型。
- `HundredQwen/api/home_page.py`：增加“生成学习资源包”、资源卡片、路径节点、引用和风险提示的最小界面。
- `HundredQwen/services/chat_prompt_service.py`：统一引用和依据不足规则；不再仅依赖自然语言提示。
- `HundredQwen/services/knowledge_base.py`：提供稳定的引用元数据接口，不改变现有检索结果格式。
- `HundredQwen/agents/orchestrator.py`：把废弃的空 `process()` 改为调用资源包服务所需的任务规划函数，或明确只保留纯任务分解，不直接持久化。
- `HundredQwen/项目功能总览.md`、`HundredQwen/项目架构文档.md`、`HundredQwen/CLAUDE.md`：同步已实现接口、主流程、新的文档路径和当前限制。
- `HundredQwen/requirements.txt`：仅在新增依赖确有必要时修改；优先使用标准库和现有依赖。

---

## Task 1：冻结主流程契约和验收数据

**Files:**
- Create: `HundredQwen/docs/superpowers/specs/2026-07-19-p0-resource-flow-design.md`
- Modify: `HundredQwen/tests/test_routes_integration.py`

- [ ] **Step 1: 写明唯一演示请求和响应契约**

固定请求：

```json
{
  "student_id": "stu_001",
  "course_name": "人工智能",
  "topic": "Transformer 注意力机制",
  "difficulty": "intermediate",
  "resource_types": ["document", "mindmap", "exercise", "reading", "code_example"]
}
```

固定响应至少包含：`bundle_id`、`student_id`、`status`、`resources`、`path`、`citations`、`safety`、`warnings`。

- [ ] **Step 2: 为主流程增加路由存在性测试**

测试以下路径存在：

```text
POST /api/generation/resource-bundle
GET  /api/generation/resource-bundles/{student_id}
GET  /api/generation/learning-path/{student_id}
PUT  /api/generation/learning-path/{path_id}/nodes/{node_id}
```

- [ ] **Step 3: 运行测试确认新契约失败**

Run: `python -m pytest -q tests/test_routes_integration.py`

Expected: 新增路径断言失败，原因是路由尚未注册。

- [ ] **Step 4: 保存设计规格并提交**

```powershell
git add docs/superpowers/specs/2026-07-19-p0-resource-flow-design.md tests/test_routes_integration.py
git commit -m "docs: define p0 resource generation flow"
```

## Task 2：补充资源包模型和兼容持久化

**Files:**
- Modify: `HundredQwen/models/resources.py`
- Test: `HundredQwen/tests/test_resource_generation_service.py`

- [ ] **Step 1: 先写资源包持久化失败测试**

测试要求：

```python
bundle = service.save_bundle(student_id, request, resources, path, citations)
loaded = service.list_bundles(student_id)
assert loaded[0]["bundle_id"] == bundle["bundle_id"]
assert len(loaded[0]["resources"]) == 5
assert loaded[0]["citations"]
```

- [ ] **Step 2: 扩展模型而不是破坏旧资源格式**

新增 `ResourceBundle`，字段固定为：

```python
@dataclass
class ResourceBundle:
    bundle_id: str
    student_id: str
    topic: str
    course_name: str
    resource_ids: list[str]
    path_id: str | None
    citations: list[dict]
    safety: dict
    status: str = "completed"
    created_at: str = ""
```

`ResourceDB._load_all()` 对旧文件缺少 `resource_bundles` 时补充空数组；旧的 `resources` 和 `learning_paths` 读取行为不变。

- [ ] **Step 3: 实现保存、读取和按学生过滤**

新增方法：

```python
save_bundle(bundle: ResourceBundle) -> None
get_bundles_by_student(student_id: str) -> list[dict]
```

- [ ] **Step 4: 运行专项测试并提交**

Run: `python -m pytest -q tests/test_resource_generation_service.py`

Expected: 资源包持久化测试通过，旧的资源模型测试不回归。

## Task 3：实现安全检查和知识库引用

**Files:**
- Create: `HundredQwen/services/content_safety_service.py`
- Create: `HundredQwen/services/citation_service.py`
- Modify: `HundredQwen/services/knowledge_base.py`
- Modify: `HundredQwen/services/chat_prompt_service.py`
- Create: `HundredQwen/tests/test_content_safety_service.py`
- Create: `HundredQwen/tests/test_citation_service.py`

- [ ] **Step 1: 写安全检查的失败测试**

覆盖三种行为：

```python
assert checker.check_input("请解释注意力机制").allowed is True
assert checker.check_input("<测试敏感词>").allowed is False
assert checker.check_output("正常教材解释").allowed is True
```

敏感词表放在 `services/content_safety_service.py` 的可注入配置中，测试不得依赖真实模型或网络。

- [ ] **Step 2: 写引用服务失败测试**

引用结果必须包含：`source_id`、`title`、`page`、`snippet`、`score`。无检索结果时返回 `evidence_level="insufficient"`，不能伪造引用。

- [ ] **Step 3: 实现最小安全层**

接口固定为：

```python
class SafetyResult:
    allowed: bool
    risk_level: str
    reason: str
    sanitized_text: str

class ContentSafetyService:
    def check_input(self, text: str) -> SafetyResult: ...
    def check_output(self, text: str) -> SafetyResult: ...
```

输入不通过时生成接口返回 HTTP 400；模型输出不通过时返回安全提示，不把原始违规内容返回给前端。

- [ ] **Step 4: 为知识库检索增加引用元数据**

`KnowledgeBase` 返回的每个 chunk 保留文档名、章节、页码、chunk id 和相似度；`CitationService.from_chunks()` 只从真实 chunk 生成引用。

- [ ] **Step 5: 将引用规则加入问答和资源生成**

有依据时在响应中返回 `citations`；无依据时返回“知识库未找到充分依据，请核验”的 warning，并要求模型使用保守表述。

- [ ] **Step 6: 运行测试并提交**

Run: `python -m pytest -q tests/test_content_safety_service.py tests/test_citation_service.py tests/test_chat_service.py`

Expected: 安全和引用测试通过，原问答测试不回归。

## Task 4：实现五类 Agent 资源包生成

**Files:**
- Create: `HundredQwen/services/resource_generation_service.py`
- Modify: `HundredQwen/services/app_services.py`
- Modify: `HundredQwen/agents/orchestrator.py`
- Modify: `HundredQwen/models/resources.py`
- Test: `HundredQwen/tests/test_resource_generation_service.py`

- [ ] **Step 1: 写 Stub Agent 协作失败测试**

用真实服务类和 Stub Agent，不调用网络。测试必须验证 5 个 Agent 都被调用，并且每个资源带有同一个 `student_id`、`course_name` 和至少一个引用/依据状态。

```python
result = service.generate_bundle(request)
assert set(result.resource_types) == {
    "document", "mindmap", "exercise", "reading", "code_example"
}
assert recorder.calls == [
    "DocumentAgent", "MindMapAgent", "ExerciseAgent",
    "ReadingAgent", "CodeExampleAgent"
]
```

- [ ] **Step 2: 定义服务入口**

```python
class ResourceGenerationService:
    def generate_bundle(self, request: ResourceBundleRequest) -> dict: ...
    def list_bundles(self, student_id: str) -> list[dict]: ...
    def get_learning_path(self, student_id: str) -> dict | None: ...
    def update_path_node(self, path_id: str, node_id: str, status: str) -> dict: ...
```

服务内部顺序固定为：验证学生 → 安全检查 → 检索依据 → 并行或顺序调用五个 Agent → 输出安全检查 → 保存资源 → 调用 `LearningPathAgent` → 保存路径 → 保存 bundle。

- [ ] **Step 3: 处理单个 Agent 失败**

单个资源失败时，不伪造成功资源；返回 `status="partial"`、失败类型和 warning。核心文档、练习题、学习路径失败时整体状态为 `failed`，并且不写入半成品 bundle。

- [ ] **Step 4: 接入 Orchestrator 的任务分解职责**

将 `Orchestrator` 的职责限定为生成资源任务计划和 Agent 顺序，不让旧的 `process()` 返回空成功结果。资源持久化统一由 `ResourceGenerationService` 完成。

- [ ] **Step 5: 装配服务并运行测试**

Run: `python -m pytest -q tests/test_resource_generation_service.py tests/test_app_services.py`

Expected: 五类 Agent 调用顺序、失败回滚、旧服务装配测试全部通过。

## Task 5：把资源包和学习路径暴露为 API

**Files:**
- Create: `HundredQwen/api/generation_routes.py`
- Modify: `HundredQwen/api/schemas.py`
- Modify: `HundredQwen/api/routes.py`
- Create: `HundredQwen/tests/test_generation_routes.py`

- [ ] **Step 1: 定义请求和响应模型**

新增模型：

```python
class ResourceBundleRequest(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    course_name: str = Field(default="人工智能", min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty: str = "intermediate"
    resource_types: list[str] = Field(
        default_factory=lambda: [
            "document", "mindmap", "exercise", "reading", "code_example"
        ]
    )
```

校验 `resource_types` 只能是五类支持类型，并拒绝空列表。

- [ ] **Step 2: 实现四个路由**

```python
@app.post("/api/generation/resource-bundle")
async def generate_resource_bundle(req, services): ...

@app.get("/api/generation/resource-bundles/{student_id}")
async def list_resource_bundles(student_id, services): ...

@app.get("/api/generation/learning-path/{student_id}")
async def get_learning_path(student_id, services): ...

@app.put("/api/generation/learning-path/{path_id}/nodes/{node_id}")
async def update_learning_path_node(path_id, node_id, req, services): ...
```

错误契约固定为：学生不存在 404、输入安全失败 400、资源生成失败 502、路径节点状态非法 422。

- [ ] **Step 3: 写接口测试**

至少覆盖：成功生成、学生不存在、非法资源类型、输入被拦截、部分失败、路径节点从 `pending` 更新到 `completed`。

- [ ] **Step 4: 运行测试并提交**

Run: `python -m pytest -q tests/test_generation_routes.py tests/test_routes_integration.py`

Expected: 新接口契约通过，旧接口路径和状态码不变。

## Task 6：实现仪表盘最小闭环界面

**Files:**
- Modify: `HundredQwen/api/home_page.py`
- Modify: `HundredQwen/tests/test_home_page.py`

- [ ] **Step 1: 增加资源包生成入口**

在仪表盘增加主题输入框和“生成个性化资源包”按钮；提交时显示“正在分析画像 / 正在生成资源 / 正在规划路径 / 已完成”四个阶段状态。

- [ ] **Step 2: 增加资源卡片**

根据 `resource_type` 渲染五类卡片：标题、难度、摘要、引用数量、打开详情。未知类型只显示通用卡片，不让页面脚本报错。

- [ ] **Step 3: 增加路径节点**

展示顺序、标题、预计时长、状态和关联资源；完成按钮调用路径节点更新接口，成功后重新加载资源包和学习时间。

- [ ] **Step 4: 增加安全和引用提示**

有风险时显示警告条；有引用时显示来源标题/章节/页码；依据不足时显示“请核验”而不是伪造来源。

- [ ] **Step 5: 增加前端契约测试**

测试 HTML 中存在生成入口、四个阶段状态、五类资源类型、引用区域和路径更新接口；不要求在 Python 单元测试中模拟完整浏览器。

- [ ] **Step 6: 手动验证页面**

启动服务后访问 `http://127.0.0.1:9010`，使用 `stu_001` 完成一次生成；确认刷新页面后资源和路径仍存在。

## Task 7：补齐运行和错误体验

**Files:**
- Modify: `HundredQwen/api/home_page.py`
- Modify: `HundredQwen/api/generation_routes.py`
- Modify: `HundredQwen/start.ps1`
- Modify: `HundredQwen/check_server.py`
- Create: `HundredQwen/tests/test_generation_resilience.py`

- [ ] **Step 1: 统一耗时操作错误显示**

前端对 400/404/422/502 分别显示用户可理解的提示；异常时恢复按钮可用状态，不留下无限 loading。

- [ ] **Step 2: 为同步生成加超时边界**

服务端对每个 Agent 调用记录开始/结束时间；超过配置阈值时返回 partial/failed 状态。不要在本阶段引入 Celery、Redis 或新的基础设施。

- [ ] **Step 3: 增加生成接口的响应日志字段**

日志至少包含：`bundle_id`、`student_id`、`agent_name`、`duration_ms`、`status`、`warning_count`。日志不得输出 API Key、密码或完整学生隐私字段。

- [ ] **Step 4: 验证服务重启工作流**

代码修改后按项目约定自动停止旧的 HundredQwen Python 进程、用 `start.ps1` 启动、请求 `/api/config/llm/status` 和资源包接口确认新代码生效；浏览器只需刷新。

## Task 8：补齐测试说明和提交文档

**Files:**
- Create: `HundredQwen/docs/需求分析说明书.md`
- Create: `HundredQwen/docs/系统开发说明书.md`
- Create: `HundredQwen/docs/测试说明书.md`
- Create: `HundredQwen/docs/部署运行说明.md`
- Create: `HundredQwen/docs/知识库与测试数据说明.md`
- Create: `HundredQwen/docs/第三方依赖与AI工具说明.md`
- Modify: `HundredQwen/项目功能总览.md`
- Modify: `HundredQwen/项目架构文档.md`
- Modify: `HundredQwen/CLAUDE.md`

- [ ] **Step 1: 编写需求分析说明书**

必须包含：目标用户、学习资源痛点、画像维度、五类资源、路径推送、安全要求、可选加分项和需求-功能映射表。

- [ ] **Step 2: 编写系统开发说明书**

必须包含：架构图、主流程图、Agent 角色表、接口表、数据模型、RAG 引用流程、安全流程、PPT/语音集成和前端交互说明。

- [ ] **Step 3: 编写测试说明书**

必须包含：测试环境、单元测试、接口测试、主流程测试、异常测试、人工验收步骤、最终测试命令和结果。测试结果必须来自新一轮实际执行，不得手填。

- [ ] **Step 4: 编写部署和数据说明**

明确 Python 版本、依赖安装、`.env` 配置、知识库目录、默认账号、启动命令、固定端口、重启规则、无 API Key 时的降级行为和常见故障。

- [ ] **Step 5: 编写第三方和 AI 工具说明**

列出 FastAPI、Pydantic、SQLite、requests、websocket、marked、highlight.js、讯飞智文、讯飞星火、DeepSeek 等名称、来源、版本和协议；明确 AI Coding 工具在需求分析、代码实现、测试和文档中的使用范围。

- [ ] **Step 6: 同步旧文档中的过时描述**

把“历史路径”“旧主链路”“7 个 Agent 已协作”等容易造成误解的描述改为实际状态，并修正旧的本机路径。

## Task 9：准备 7 分钟演示和最终门禁

**Files:**
- Create: `HundredQwen/docs/演示脚本.md`
- Create: `HundredQwen/docs/提交前检查清单.md`

- [ ] **Step 1: 固定 7 分钟时间轴**

```text
00:00-00:35  项目价值和用户痛点
00:35-01:20  登录并展示学生画像
01:20-02:00  输入学习需求并展示知识库引用
02:00-04:10  展示五类 Agent 资源生成结果
04:10-05:00  展示个性化学习路径和资源关联
05:00-05:45  完成一道练习并更新学习进度
05:45-06:25  开始/暂停学习并展示仪表盘统计
06:25-07:00  总结多智能体协作、前沿 AI 集成和创新点
```

- [ ] **Step 2: 准备可复现演示数据**

固定 `stu_001`、固定主题、固定知识库文档和无网络失败备用截图/录屏；演示前清理上次生成的临时资源，但保留默认画像和 26 小时学习时间。

- [ ] **Step 3: 执行最终门禁**

Run:

```powershell
python -m pytest -q
python check_server.py
Invoke-WebRequest http://127.0.0.1:9010/api/knowledge/stats
Invoke-WebRequest http://127.0.0.1:9010/api/resources/stu_001
```

Expected：全量测试 0 failures；服务健康；知识库有文档和 chunks；资源包生成后资源接口不为空；无未处理异常、无限 loading 或 404 主流程接口。

- [ ] **Step 4: 完成提交清单**

检查源码、知识库/测试数据、模型配置模板、文档、PPT、视频、许可证和 AI 工具说明均在提交目录中；`.env` 中真实密钥不得进入提交包。

## 三、建议执行顺序和里程碑

### 里程碑 M1：后端闭环

完成 Task 1–5。验收标准：使用 Stub Agent 的自动测试可以证明五类资源被调用、被保存、生成路径并能通过 API 读取。

### 里程碑 M2：前端可演示

完成 Task 6–7。验收标准：浏览器中可以从一个入口完成生成、查看五类资源、查看路径、完成节点、查看引用和安全提示；刷新后数据仍在。

### 里程碑 M3：可提交

完成 Task 8–9。验收标准：陌生环境按部署文档可以启动；7 分钟脚本可以走完；测试说明书和实际输出一致；所有第三方和 AI 工具均有说明。

## 四、风险和取舍

1. **真实模型输出不稳定**：自动化测试全部使用 Stub Agent；人工验收使用固定主题和本地知识库，真实模型失败时必须显示 partial/failed，不得伪造成功。
2. **生成时间过长**：P0 不引入新任务队列，先使用阶段状态、超时和错误恢复；如果真实模型仍超过演示窗口，再单独制定异步任务计划。
3. **JSON 资源并发写入**：P0 保留现有 `ResourceDB`，演示场景单用户运行；若后续支持并发，再将资源和路径迁移 SQLite。
4. **知识库依据不足**：宁可显示“依据不足”，不要生成无来源引用；演示主题必须来自已有教材内容。
5. **文档与代码漂移**：每个里程碑结束后同步文档，并在最终测试说明书中记录实际命令和输出。

## 五、完成定义

只有同时满足以下条件，P0 才算完成：

- [ ] 五类资源由五个不同 Agent 在同一资源包请求中实际被调用。
- [ ] 资源和学习路径持久化，刷新或重启服务后仍可读取。
- [ ] 主流程展示引用、依据不足提示和安全检查结果。
- [ ] 生成失败会返回明确状态，前端按钮和加载状态可恢复。
- [ ] 全量测试通过，且有主流程接口和人工验收记录。
- [ ] 系统开发、测试、部署、数据、依赖/协议、AI 工具说明文档齐全。
- [ ] 7 分钟演示脚本可在常规环境执行，提交包不包含真实密钥。
