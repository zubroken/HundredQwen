"""
练习题生成智能体 —— 生成多种类型练习题目
"""
from __future__ import annotations
import logging
from typing import Optional

from agents.base_agent import BaseAgent, AgentMessage
from models.resources import ExerciseResource, ExerciseType
from services.llm_service import LLMService
from services.model_gateway import ModelGateway
from utils.helpers import generate_id, now_str, safe_json_parse

logger = logging.getLogger(__name__)


class ExerciseAgent(BaseAgent):
    """
    练习智能体 —— 根据学生薄弱点生成针对性练习题
    支持选择题、填空题、简答题、编程题、判断题等多种类型
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        model_gateway: Optional[ModelGateway] = None,
    ):
        super().__init__(
            name="ExerciseAgent",
            role_description="你是练习题生成专家。擅长根据学生的知识短板和易错点，"
                             "生成针对性的练习题目。支持多种题型：选择题、填空题、简答题、"
                             "编程题、判断题。题目难度应根据学生当前水平分层设置，"
                             "并提供详细的答案解析，帮助学生巩固知识点。",
            llm_service=llm_service,
        )
        self.model_gateway = model_gateway

    def generate_exercises(self, profile, request: str) -> ExerciseResource:
        """生成个性化练习题"""
        profile_context = self._format_profile_context(profile)

        system_prompt = self.get_system_prompt() + f"""
        基于以下学生画像，针对学生的薄弱知识点生成一套练习题目。
        {profile_context}
        特别关注学生的薄弱点：{', '.join(profile.weak_points) if profile.weak_points else '根据请求内容判断'}

        请返回JSON格式（不要包含```标记），包含以下字段：
        {{
            "title": "练习标题",
            "exercise_type": "mixed",
            "questions": [
                {{
                    "type": "choice/fill_blank/short_answer/coding/true_false",
                    "difficulty": "easy/medium/hard",
                    "stem": "题目内容",
                    "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
                    "answer": "正确答案",
                    "explanation": "详细解析"
                }}
            ],
            "total_score": 总分,
            "estimated_time_minutes": 预计用时
        }}
        至少生成3-5道题目，包含至少2种不同的题型，难度递进。
        """

        backend = self.model_gateway.get() if self.model_gateway else self.llm
        response = backend.chat(system_prompt, request)
        data = safe_json_parse(response) or {}

        resource = ExerciseResource(
            resource_id=generate_id("ex"),
            title=data.get("title", "针对性练习"),
            content=data,
            tags=profile.weak_points,
            difficulty="beginner",
            course_name=request[:50],
            created_at=now_str(),
            student_id=profile.student_id,
        )

        logger.info(f"Exercises generated: {resource.resource_id}")
        return resource

    def process(self) -> Optional[AgentMessage]:
        for msg in self.mailbox:
            if msg.message_type == "request":
                profile = msg.content.get("profile") if isinstance(msg.content, dict) else None
                request = msg.content.get("request", "") if isinstance(msg.content, dict) else str(msg.content)
                if not profile:
                    return AgentMessage(sender=self.name, receiver=msg.sender,
                                        message_type="response", content=None)
                ex = self.generate_exercises(profile, request)
                return AgentMessage(sender=self.name, receiver=msg.sender,
                                    message_type="response", content=ex)
        self.mailbox.clear()
        return None
