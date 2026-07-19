# 变更日志 — 2026-05-14

## 背景

项目原支持三种 LLM provider（OpenAI、Anthropic、Mock），但经排查：
- .env 中仅配置了 DeepSeek API Key
- OpenAI 原生和 Anthropic 均无有效 Key
- Mock 模式为假数据，不产生实际价值

因此决定精简 LLM 层，移除无效 provider，为后续接入讯飞星火（Spark）和讯飞智文 PPT 生成铺路。

---

## 已完成的变更

### 1. `services/llm_service.py` — LLM 服务层精简

**变更前：** 策略模式，支持 OpenAI / Anthropic / Mock 三种 provider，通过 `LLMConfig.provider` 字段切换。

**变更后：** 精简为 DeepSeek 单一后端，通过 OpenAI 兼容 SDK 调用。

- 移除 `LLMConfig.provider` 字段
- 移除 `_call_openai()` / `_call_anthropic()` / `_mock_response()` 三个方法
- 移除 Anthropic SDK 导入和客户端初始化逻辑
- 移除 Mock 降级逻辑
- 新增 `LLMConfig.base_url` 字段（默认 `https://api.deepseek.com/v1`）
- 聊天方法 `chat()` 直接内联调用 DeepSeek

### 2. `main.py` — 入口简化

**变更前：** 支持 `--provider mock|openai|anthropic` 三选一切换。

**变更后：**
- 移除 `--provider` 参数
- 默认 LLM 固定为 DeepSeek
- 保留 `--model`、`--api-key`、`--host`、`--port` 参数
- 版本号升至 v1.0.4

### 3. `api/routes.py` — 路由层适配

**变更前：** `LLMConfigRequest` 包含 `provider` 字段，热切换端点根据 provider 创建客户端。

**变更后：**
- `LLMConfigRequest` 移除 `provider`，新增 `base_url`
- `/api/config/llm` 端点适配新的 `LLMConfig` 结构

### 4. `.env` — 环境变量整理

**变更前：** 使用通用的 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`（实际指向 DeepSeek）。

**变更后：**
- 改用 `DEEPSEEK_API_KEY` 和 `DEEPSEEK_BASE_URL`
- 预留了讯飞星火（Spark）配置占位：`SPARK_APP_ID`、`SPARK_API_KEY`、`SPARK_API_SECRET`

### 5. `CLAUDE.md` — 项目文档更新

- 更新启动命令，移除 Mock/OpenAI/Anthropic 相关示例
- 更新架构描述，标注 LLM 层已精简为 DeepSeek 单一后端

---

## 接口兼容性

| 接口 | 影响 |
|------|------|
| `LLMService(LLMConfig(...))` | `LLMConfig` 不再需要 `provider` 参数 |
| `llm_service.chat(system, user)` | 签名不变，内部直接调用 DeepSeek |
| `llm_service.chat_json(system, user)` | 签名不变 |
| `python main.py` | 无需再传 `--provider`，默认 DeepSeek |

所有现有 Agent（ProfileAgent、DocumentAgent、ExerciseAgent 等）无需修改，它们通过 `llm_service.chat()` 调用，接口未变。

---

## 下一步计划

- [ ] 接入科大讯飞星火（Spark）大模型
- [ ] 集成讯飞智文（Zhiwen）PPT 生成功能
- [ ] 前端新增 PPT 生成入口
