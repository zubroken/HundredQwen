# P0 学习工作台设计规格

## 目标

在保留 HundredQwen 现有侧边栏、用户卡片、仪表盘概览和技能树入口的前提下，将仪表盘扩展为可演示的学习工作台。用户输入一个学习主题后，系统基于学生画像和本地知识库生成五类资源、学习路径、引用信息和安全状态；刷新页面后资源和路径仍可读取。

## 非目标

- 不拆分当前内嵌 SPA。
- 不引入 Celery、Redis 或新的云服务。
- 不实现正式多用户授权和生产级审计。
- 不承诺真实视频/动画生成；P0 的多模态展示以文档、结构化思维导图、练习、阅读、代码案例、PPT/语音已有能力为主。

## 界面设计

### 保留区域

- 原有侧边栏、登录/注册、个人画像、聊天、知识库、PPT、技能树和学习时间功能。
- 仪表盘顶部概览卡片继续展示学习时间、资源概览、最近学习和技能树入口。
- 现有蓝色主色、卡片层级和 SVG 图标体系保持一致。

### 新增学习工作台区域

仪表盘概览下新增一个区域，按以下顺序排列：

```text
学习主题输入框 + 唯一主按钮“生成个性化资源包”
生成阶段状态：分析画像 → 检索教材依据 → 生成五类资源 → 规划学习路径
左栏：五类资源卡片
右栏：学习路径、当前节点、本周学习时间
```

桌面宽度下资源区与路径区两栏显示；小屏幕下按“生成区 → 路径 → 资源”单列显示。按钮、路径完成控件和资源详情入口有可见焦点，文字与背景对比度达到 WCAG AA；加载超过 300ms 时展示稳定的阶段状态，不使用无限旋转等待。

### 资源卡片

固定支持五种资源：`document`、`mindmap`、`exercise`、`reading`、`code_example`。每张卡片展示标题、难度、摘要、引用数量和详情入口。引用存在时列出教材名、章节/页码和片段；依据不足时显示“知识库未找到充分依据，请核验”，不显示伪造来源。

## 后端设计

新增 `ResourceGenerationService` 作为资源包主模块，调用方只需使用以下接口：

```python
generate_bundle(request) -> dict
list_bundles(student_id) -> list[dict]
get_learning_path(student_id) -> dict | None
update_path_node(path_id, node_id, status) -> dict
```

该模块内部负责：

```text
验证学生
→ 输入安全检查
→ 基于主题、薄弱点和课程检索知识库
→ 从检索结果创建真实引用
→ 调用文档、导图、练习、阅读、代码五个 Agent
→ 对 Agent 输出进行安全检查
→ 保存五类资源
→ 调用 LearningPathAgent 生成路径并保存
→ 保存资源包并返回
```

`Orchestrator` 只负责输出资源生成任务计划和 Agent 调用顺序；资源保存、路径保存和错误汇总全部由 `ResourceGenerationService` 处理，避免旧编排器与新服务同时写入资源库。

## 数据与接口

在现有 `ResourceDB` JSON 文件中新增 `resource_bundles` 数组，旧的 `resources` 和 `learning_paths` 保持兼容。每个资源包至少保存：

```json
{
  "bundle_id": "bundle_xxx",
  "student_id": "stu_001",
  "topic": "Transformer 注意力机制",
  "course_name": "人工智能",
  "resource_ids": ["..."],
  "path_id": "path_xxx",
  "citations": [],
  "safety": {"risk_level": "low"},
  "status": "completed",
  "created_at": "..."
}
```

新增 API：

```text
POST /api/generation/resource-bundle
GET  /api/generation/resource-bundles/{student_id}
GET  /api/generation/learning-path/{student_id}
PUT  /api/generation/learning-path/{path_id}/nodes/{node_id}
```

请求中的资源类型只接受五类标准值。学生不存在返回 404；输入安全失败返回 400；非法资源类型或节点状态返回 422；核心资源或路径生成失败返回 502。

## 可靠性与降级

默认策略是“真实模型优先，本地知识库确定性降级”：

- 模型可用时，由真实 Agent 生成资源。
- 非核心资源失败时，保留已成功资源，将资源包标记为 `partial` 并显示失败类型。
- 文档、练习题或学习路径失败时，资源包标记为 `failed` 且不保存半成品。
- 模型整体不可用时，从本地知识库 chunk 构造确定性资源：教材摘要文档、层级导图、依据片段练习、阅读清单和最小代码案例；结果标记 `fallback=true`。
- 所有生成阶段记录 `bundle_id`、Agent 名称、耗时、状态和 warning 数量，不记录密钥、密码或完整画像正文。

## 安全与引用

新增独立的内容安全模块，对输入和输出分别返回 `allowed`、`risk_level`、`reason`、`sanitized_text`。被阻止的输入不调用模型；被阻止的输出不返回原文。引用模块只从真实知识库 chunk 构造引用，引用字段为 `source_id`、`title`、`page`、`snippet`、`score`。无 chunk 时必须设置 `evidence_level="insufficient"`。

## 测试与验收

自动化测试使用 Stub Agent，绝不依赖真实网络模型。必须覆盖：

- 五类 Agent 都在同一请求中被调用。
- 资源、路径和资源包持久化后可重新读取。
- 非核心 Agent 失败产生 `partial`；核心失败不产生半成品。
- 敏感输入被阻止，正常输入可继续。
- 引用只能来自真实 chunk，无依据时有警告。
- API 状态码契约正确。
- 前端 HTML 包含生成入口、阶段状态、资源卡片、路径状态、引用和错误提示区域。

人工验收固定使用 `stu_001` 和“Transformer 注意力机制”：生成资源包、查看五类资源、完成一个路径节点、开始/暂停学习、刷新页面确认数据仍然存在。

## 成功标准

P0 仅在以下条件同时成立时完成：五个 Agent 在同一资源包请求中实际参与；资源和路径在刷新/重启后可读取；界面明确显示引用和安全状态；生成失败可恢复；全量测试通过；开发、测试、部署、数据、第三方依赖与 AI 工具说明、演示脚本均已完成。
