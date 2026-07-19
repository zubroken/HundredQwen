from __future__ import annotations

from models.profile import StudentProfile
from services.knowledge_base import KnowledgeBase


class ChatPromptService:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def build_kb_context(self, message: str) -> str:
        chunks = self.knowledge_base.retrieve(message, top_k=3)
        if not chunks:
            return ""
        return (
            "\n【参考资料（来自教材知识库，请基于以下内容回答，并在回复中提及引用的教材名称）】\n"
            + self.knowledge_base.format_context(chunks)
        )

    def build_system_prompt(
        self,
        profile: StudentProfile,
        hist_context: str,
        kb_context: str,
    ) -> str:
        return f"""你是百问助手，专注于人工智能领域的AI学习辅导老师。
当前学生完整画像：
- 姓名：{profile.name}
- 专业：{profile.major or '人工智能'}
- 年级：{profile.grade}
- 知识基础：{profile.knowledge_base}
- 认知风格：{profile.cognitive_style or '未设定'}
- 薄弱知识点：{', '.join(profile.weak_points) if profile.weak_points else '未设定'}
- 学习目标：{', '.join(profile.learning_goals) if profile.learning_goals else '未设定'}
- 学习节奏：{profile.learning_pace or '未设定'}
- 兴趣方向：{', '.join(profile.interest_topics) if profile.interest_topics else '未设定'}
- 偏好资源类型：{', '.join(profile.preferred_resource_types) if profile.preferred_resource_types else '未设定'}
- 编程经验：{profile.programming_exp or '未设定'}
{hist_context}
{kb_context}
请遵守以下规则：
1. 只进行文本对话，不生成文档、图片、思维导图等资源
2. 回答内容聚焦人工智能领域（机器学习、深度学习、NLP、CV、强化学习等）
3. 根据学生的认知风格、薄弱知识点和学习节奏个性化调整回答方式
4. 如果【参考资料】中有相关内容，请优先基于教材回答，并明确标注引用的教材名称（如"根据《人工智能导论》..."）
5. 使用中文回复，简洁有针对性"""
