"""
画像构建智能体 —— 通过对话式交互构建动态学生画像
支持不少于6个维度的画像维度
"""
from __future__ import annotations
import logging
from typing import Optional, Dict, Any, List

from agents.base_agent import BaseAgent, AgentMessage
from models.profile import StudentProfile
from services.llm_service import LLMService
from services.model_gateway import ModelGateway
from utils.helpers import generate_id, now_str, safe_json_parse

logger = logging.getLogger(__name__)


class ProfileAgent(BaseAgent):
    """
    画像构建智能体
    通过自然语言对话自动抽取学生特征，构建多维动态画像
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        model_gateway: Optional[ModelGateway] = None,
    ):
        super().__init__(
            name="ProfileAgent",
            role_description="你是学生画像构建专家。通过与学生进行自然语言对话，"
                             "自动抽取学生的学习特征，构建包含以下维度的动态学生画像："
                             "1) 知识基础（先修课程掌握程度）"
                             "2) 认知风格（视觉型/听觉型/读写型/动觉型）"
                             "3) 薄弱知识点/易错点"
                             "4) 学习目标（短期和长期）"
                             "5) 学习进度偏好"
                             "6) 兴趣方向"
                             "7) 偏好资源类型"
                             "8) 编程/专业经验水平。"
                             "使用对话方式而非表单，让交流自然流畅。",
            llm_service=llm_service,
        )
        self.model_gateway = model_gateway

    def build_profile_from_dialogue(self, dialogue_history: List[Dict]) -> StudentProfile:
        """
        从对话历史中抽取学生特征，构建画像
        """
        dialogue_text = "\n".join([
            f"{'学生' if m.get('role') == 'user' else '系统'}: {m.get('content', '')}"
            for m in dialogue_history[-20:]  # 最近20轮对话
        ])

        system_prompt = self.get_system_prompt() + """
        从以下对话中提取学生特征，返回JSON格式（不要包含```标记）：
        {
            "knowledge_base": "知识基础描述",
            "cognitive_style": "认知风格",
            "weak_points": ["弱点1", "弱点2"],
            "learning_goals": ["目标1", "目标2"],
            "learning_pace": "快/中/慢",
            "interest_topics": ["兴趣1", "兴趣2"],
            "preferred_resource_types": ["类型1", "类型2"],
            "programming_exp": "编程经验描述"
        }
        如果某维度信息不足，请基于已知信息进行合理推断，不要留空。
        """

        backend = self.model_gateway.get() if self.model_gateway else self.llm
        response = backend.chat(system_prompt, dialogue_text)
        data = safe_json_parse(response) or {}

        profile = StudentProfile()
        profile.student_id = generate_id("stu")
        profile.knowledge_base = data.get("knowledge_base", "")
        profile.cognitive_style = data.get("cognitive_style", "")
        profile.weak_points = data.get("weak_points", [])
        profile.learning_goals = data.get("learning_goals", [])
        profile.learning_pace = data.get("learning_pace", "")
        profile.interest_topics = data.get("interest_topics", [])
        profile.preferred_resource_types = data.get("preferred_resource_types", [])
        profile.programming_exp = data.get("programming_exp", "")
        profile.created_at = now_str()
        profile.updated_at = now_str()
        profile.conversation_history = dialogue_history

        logger.info(f"Profile built for student: {profile.student_id}")
        return profile

    def update_profile(self, profile: StudentProfile,
                       new_dialogue: List[Dict]) -> StudentProfile:
        """
        根据新的对话更新画像（随学随新）
        """
        profile.conversation_history.extend(new_dialogue)
        return self.build_profile_from_dialogue(profile.conversation_history)

    def get_initial_questions(self) -> List[str]:
        """返回画像构建的初始引导问题"""
        return [
            "你好！我是你的专属学习助手。请问你主修什么专业？目前在学习哪些课程？",
            "你平时更喜欢通过什么方式学习呢？看视频、阅读文字、动手实践还是听讲解？",
            "在学习过程中，你觉得自己在哪些知识点上比较容易遇到困难？",
        ]

    def process(self) -> Optional[AgentMessage]:
        for msg in self.mailbox:
            if msg.message_type == "request":
                profile = msg.content.get("profile") if isinstance(msg.content, dict) else None
                request = msg.content.get("request", "") if isinstance(msg.content, dict) else str(msg.content)
                dialogue = msg.content.get("dialogue", []) if isinstance(msg.content, dict) else []

                # 构建或更新画像
                if dialogue:
                    if profile and profile.student_id:
                        updated = self.update_profile(profile, dialogue)
                    else:
                        updated = self.build_profile_from_dialogue(dialogue)
                else:
                    # 从请求文本中构建
                    if profile and profile.student_id:
                        updated = self.update_profile(profile, [{"role": "user", "content": request}])
                    else:
                        updated = self.build_profile_from_dialogue([{"role": "user", "content": request}])

                return AgentMessage(
                    sender=self.name,
                    receiver=msg.sender,
                    message_type="response",
                    content=updated,
                )
        self.mailbox.clear()
        return None
