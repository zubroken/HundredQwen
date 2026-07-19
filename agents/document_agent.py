"""
课程文档生成智能体 —— 生成专业课程讲解文档
"""
from __future__ import annotations
import logging
from typing import Optional

from agents.base_agent import BaseAgent, AgentMessage
from models.resources import DocumentResource
from services.llm_service import LLMService
from services.model_gateway import ModelGateway
from utils.helpers import generate_id, now_str, safe_json_parse

logger = logging.getLogger(__name__)


class DocumentAgent(BaseAgent):
    """
    文档智能体 —— 根据学生画像生成个性化的课程讲解文档
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        model_gateway: Optional[ModelGateway] = None,
    ):
        super().__init__(
            name="DocumentAgent",
            role_description="你是课程文档生成专家。根据学生的专业背景、知识基础和认知风格，"
                             "生成个性化的专业课程讲解文档。文档应结构清晰、深入浅出，"
                             "包含核心概念讲解、算法原理推导、应用场景分析等部分。"
                             "根据不同学生的知识水平调整内容的深度和广度。",
            llm_service=llm_service,
        )
        self.model_gateway = model_gateway

    def generate_document(self, profile, request: str) -> DocumentResource:
        """生成个性化讲解文档"""
        profile_context = self._format_profile_context(profile)

        system_prompt = self.get_system_prompt() + f"""
        基于以下学生画像，为学生的具体学习需求生成一份个性化的课程讲解文档。
        {profile_context}

        请返回JSON格式（不要包含```标记），包含以下字段：
        {{
            "title": "文档标题",
            "sections": [
                {{"title": "节标题", "content": "详细内容", "level": 1}},
                ...
            ],
            "summary": "文档总结",
            "prerequisites": ["预备知识1", "预备知识2"],
            "key_concepts": ["核心概念1", "核心概念2"],
            "references": ["参考资源1", "参考资源2"]
        }}
        内容应当使用中文，根据学生的认知风格调整呈现方式（视觉型多用结构化描述，读写型提供详细文字）。
        """

        backend = self.model_gateway.get() if self.model_gateway else self.llm
        response = backend.chat(system_prompt, request)
        data = safe_json_parse(response) or {}

        resource = DocumentResource(
            resource_id=generate_id("doc"),
            title=data.get("title", f"课程讲解文档"),
            content=data,
            tags=data.get("key_concepts", []),
            course_name=request[:50],
            created_at=now_str(),
            student_id=profile.student_id,
        )

        logger.info(f"Document generated: {resource.resource_id}")
        return resource

    def process(self) -> Optional[AgentMessage]:
        for msg in self.mailbox:
            if msg.message_type == "request":
                profile = msg.content.get("profile") if isinstance(msg.content, dict) else None
                request = msg.content.get("request", "") if isinstance(msg.content, dict) else str(msg.content)

                if not profile:
                    return AgentMessage(sender=self.name, receiver=msg.sender,
                                        message_type="response", content=None)

                doc = self.generate_document(profile, request)
                return AgentMessage(
                    sender=self.name,
                    receiver=msg.sender,
                    message_type="response",
                    content=doc,
                )
        self.mailbox.clear()
        return None
