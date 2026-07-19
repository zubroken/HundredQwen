# 讯飞大模型中文语音识别（WebSocket 流式）设计方案

> 百问即查项目 — 基于讯飞官方 Demo 和接口文档的语音输入功能
> 参考：`大模型中文语音识别.py`（官方 Demo）、`接口要求与更多.md`（官方文档）

## 一、适用场景

| 面板 | 麦克风位置 | 用途 |
|------|-----------|------|
| 智能问答 | 聊天输入框左侧 | 语音提问 |
| 知识库查询 | 搜索框左侧 | 语音搜教材/概念 |
| PPT 生成 | 主题输入框左侧 | 语音说 PPT 主题 |
| 做练习题 | 简答题作答区 | 语音回答 |

## 二、技术方案

### 2.1 架构决策

讯飞大模型中文语音识别**仅支持 WebSocket 流式协议**（`wss://iat.xf-yun.com/v1`），不存在 REST 端点。前后端分工：

```
浏览器                        Python 后端                       讯飞
──────                        ──────────                       ────
MediaRecorder 录音            POST 接收音频                  WebSocket
→ Blob (audio/webm)          → ffmpeg 转 PCM (16kHz)         流式上传帧
→ fetch POST /api/speech     → 拼接 HMAC-SHA256 鉴权 URL    → 接收识别结果
                              → ws 连接讯飞，逐帧发送        → 返回 JSON
                              → 收集文本片段
                              ← return {"text": "完整文本"}
→ 填入输入框
```

**前端：简单 POST（一次上传）→ 后端：WebSocket 流式（对接讯飞）**

用户体感：点麦克风→说话→点停止→等待1-2秒→文字出现

### 2.2 核心依赖

| 依赖 | 用途 | 安装方式 |
|------|------|---------|
| `websocket-client` | Python 端 WebSocket 客户端连接讯飞 | `pip install websocket-client` |
| `ffmpeg` | 将浏览器 audio/webm 转为 16kHz PCM | 系统安装（`choco install ffmpeg` 或官网下载） |

### 2.3 讯飞 API 协议参数

| 参数 | 固定值 | 说明 |
|------|--------|------|
| 地址 | `wss://iat.xf-yun.com/v1` | 中英文语音识别 |
| 鉴权 | HMAC-SHA256 → URL 参数 `?authorization=&date=&host=` | 参考接口文档第四节 |
| domain | `slm` | 大模型中文语音识别 |
| language | `zh_cn` | 中英文混合 |
| accent | `mandarin` | 普通话 |
| dwa | `wpgs` | 动态修正（边说边改，最终结果更准） |
| encoding | `raw` | PCM 原始音频 |
| sample_rate | `16000` | 16kHz 采样率 |
| channels | `1` | 单声道 |
| bit_depth | `16` | 16bit 位深 |

### 2.4 数据发送规范（来自官方文档）

- 帧大小：**1280 字节/帧**
- 发送间隔：**40ms/帧**
- 帧状态：0=首帧（带参数）、1=中间帧（纯音频）、2=末帧（空音频）
- 最大时长：**60 秒**

### 2.5 识别结果解析（来自官方 Demo）

```python
# 收到的 JSON 中 payload.result.text 是 base64 编码的
text = base64.b64decode(payload["result"]["text"])
data = json.loads(text)
# data["ws"] 是词序列，每个词有 cw[].w 字段
for word_group in data["ws"]:
    for char_item in word_group["cw"]:
        result += char_item["w"]
```

## 三、文件变更清单

### 3.1 新增文件

**`services/speech_service.py`**（~120 行）

核心类 `SpeechService`：

```python
class SpeechService:
    APP_ID / API_KEY / API_SECRET  # 从 .env 读取

    def _build_url():
        # HMAC-SHA256 签名，生成鉴权 URL
        # 完全复用官方 Demo 的 create_url() 逻辑

    def _send_audio_frames(ws, pcm_path):
        # 读取 PCM 文件，按 1280 字节分帧
        # 每 40ms 发一帧，status=0/1/2
        # 复用官方 Demo 的 on_open() 逻辑

    def recognize(audio_bytes: bytes) -> str:
        # 1. 写临时 webm 文件
        # 2. ffmpeg 转 16kHz PCM (subprocess)
        # 3. 连接 wss，发送帧
        # 4. 收集 on_message 回调的识别结果
        # 5. 清理临时文件
        # 6. 返回完整文本
```

**`services/speech_service.py`** 依赖 `websocket-client` + `threading`（demo 用 `_thread`，生产改用 `threading`）。

### 3.2 修改文件

| 文件 | 改动 |
|------|------|
| `services/app_services.py` | 注册 SpeechService |
| `api/learning_routes.py` | 新增 `POST /api/speech/recognize` 端点 |
| `api/home_page.py` | 聊天框 KB PPT 练习题 四个输入框各加麦克风按钮 + CSS + JS |
| `requirements.txt` | 新增 `websocket-client` |
| `.env` | 确保 `SPARK_APP_ID`, `SPARK_API_KEY`, `SPARK_API_SECRET` 三个字段存在 |

### 3.3 鉴权复用

语音听写使用的 APP_ID / API_KEY / API_SECRET 与现有 Spark LLM、智文 PPT 是 **同一套讯飞控制台凭证**（三个字段 `.env` 中已配置）。

签名算法与官方 Demo 完全一致，不与 `zhiwen_service.py` 的 HMAC-SHA1 冲突。

## 四、前端 UI

### 4.1 麦克风按钮

```
┌─────────────────────────────────────────┐
│ [🎤] [输入你的问题..._______________] [发送]│
│  ↑ 灰色圆按钮 36x36，三种状态切换           │
└─────────────────────────────────────────┘
```

### 4.2 三种状态

| 状态 | CSS | 描述 |
|------|-----|------|
| 空闲 | `.mic-btn` 灰色 | 默认 |
| 录音中 | `.mic-btn.recording` 红色脉冲 `@keyframes pulse` | input placeholder → "正在聆听..." |
| 识别中 | `.mic-btn.processing` 蓝色旋转 | input placeholder → "识别中..." |

### 4.3 前端 JS 关键函数

```javascript
async function startMic(inputId) {
  // getUserMedia → MediaRecorder → ondataavailable 拿 Blob
  // 改按钮 CSS + placeholder
}
async function stopMic() {
  // MediaRecorder.stop() → POST /api/speech/recognize → 填入 input
  // 恢复按钮 CSS + placeholder
}
```

## 五、测试策略

1. **单元测试**：`test_speech_service.py` — 签名 URL 生成正确性
2. **集成测试**：准备一个 16kHz PCM 测试音频文件，调 `recognize()`，验证返回文本非空
3. **手动测试**：浏览器点麦克风 → 说中文/英文 → 看文字是否填入输入框
4. **边界测试**：空录音、超 60s、无麦克风权限、网络中断

## 六、开发步骤

1. 安装依赖：`pip install websocket-client` + 系统装 ffmpeg
2. 创建 `services/speech_service.py`（HMAC-SHA256 签名 + WebSocket 帧发送 + 结果收集）
3. `services/app_services.py` 注册 SpeechService
4. `api/learning_routes.py` 加 `POST /api/speech/recognize`
5. `api/home_page.py` 四个面板各加麦克风按钮 + CSS 状态动画 + JS 录音逻辑
6. `python -m pytest tests/ -v` 确保 62 测试不回归
7. 浏览器手动测试完整流程
