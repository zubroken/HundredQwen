"""
拓展阅读智能体 —— 生成个性化拓展阅读材料
"""
from __future__ import annotations
import logging
from typing import Optional

from agents.base_agent import BaseAgent, AgentMessage
from models.resources import ReadingResource
from services.llm_service import LLMService
from services.model_gateway import ModelGateway
from utils.helpers import generate_id, now_str, safe_json_parse

logger = logging.getLogger(__name__)


class ReadingAgent(BaseAgent):
    """
    阅读智能体 —— 根据学生兴趣和知识水平推荐拓展阅读材料
    包括论文、技术博客、书籍章节等
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        model_gateway: Optional[ModelGateway] = None,
    ):
        super().__init__(
            name="ReadingAgent",
            role_description="你是拓展阅读推荐专家。根据学生的专业方向、兴趣领域和当前知识水平，"
                             "推荐适合的拓展阅读材料，包括经典教材、前沿论文、技术博客、"
                             "开源项目文档等。每份推荐应说明其与学习内容的相关性及推荐理由。",
            llm_service=llm_service,
        )
        self.model_gateway = model_gateway

    def generate_readings(self, profile, request: str) -> ReadingResource:
        """生成个性化拓展阅读材料"""
        profile_context = self._format_profile_context(profile)

        system_prompt = self.get_system_prompt() + f"""
        基于以下学生画像，生成个性化的拓展阅读推荐。
        {profile_context}
        学生的兴趣方向：{', '.join(profile.interest_topics) if profile.interest_topics else '根据请求内容判断'}

        请返回JSON格式（不要包含```标记），包含以下字段：
        {{
            "title": "推荐标题",
            "materials": [
                {{
                    "title": "材料名称",
                    "type": "教材/论文/博客/文档/视频",
                    "summary": "内容简介",
                    "relevance": "与学习内容的相关性说明"
                }}
            ],
            "reading_guide": "阅读顺序和建议",
            "discussion_points": ["思考点1", "思考点2"]
        }}
        至少推荐3-5份材料，覆盖不同类型。
        """

        backend = self.model_gateway.get() if self.model_gateway else self.llm
        response = backend.chat(system_prompt, request)
        data = safe_json_parse(response) or {}

        resource = ReadingResource(
            resource_id=generate_id("read"),
            title=data.get("title", "拓展阅读推荐"),
            content=data,
            tags=profile.interest_topics,
            course_name=request[:50],
            created_at=now_str(),
            student_id=profile.student_id,
        )

        logger.info(f"Reading materials generated: {resource.resource_id}")
        return resource

    def process(self) -> Optional[AgentMessage]:
        for msg in self.mailbox:
            if msg.message_type == "request":
                profile = msg.content.get("profile") if isinstance(msg.content, dict) else None
                request = msg.content.get("request", "") if isinstance(msg.content, dict) else str(msg.content)
                if not profile:
                    return AgentMessage(sender=self.name, receiver=msg.sender,
                                        message_type="response", content=None)
                reading = self.generate_readings(profile, request)
                return AgentMessage(sender=self.name, receiver=msg.sender,
                                    message_type="response", content=reading)
        self.mailbox.clear()
        return None
