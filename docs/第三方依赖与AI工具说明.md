# HundredQwen 第三方依赖与 AI 工具说明

## 后端依赖

- FastAPI：Web API 框架
- Pydantic：请求数据校验
- Uvicorn：本地 ASGI 服务
- SQLite：学生画像和学习进度存储
- pdfplumber：PDF 文本提取
- jieba：中文关键词提取
- requests / websockets：外部模型或语音服务调用

## 前端依赖

- marked：Markdown 渲染
- highlight.js：代码高亮
- canvas-confetti：练习反馈动效

## AI 服务

- DeepSeek：默认文本模型后端
- 讯飞星火：可选模型后端
- 讯飞智文：PPT 生成服务

## AI Coding 使用说明

本项目在需求分析、方案设计、代码实现、测试补充、文档整理和本地验证中使用 AI 编程助手 Codex。涉及真实业务输出时，系统通过知识库引用、安全检查和 fallback 机制降低幻觉风险。
