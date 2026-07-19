"""
思维导图生成智能体 —— 生成知识点思维导图
"""
from __future__ import annotations
import logging
from typing import Optional

from agents.base_agent import BaseAgent, AgentMessage
from models.resources import MindMapResource
from services.llm_service import LLMService
from services.model_gateway import ModelGateway
from utils.helpers import generate_id, now_str, safe_json_parse

logger = logging.getLogger(__name__)


class MindMapAgent(BaseAgent):
    """
    思维导图智能体 —— 根据知识点生成结构化的思维导图
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        model_gateway: Optional[ModelGateway] = None,
    ):
        super().__init__(
            name="MindMapAgent",
            role_description="你是思维导图生成专家。擅长将复杂的知识点进行结构化梳理，"
                             "生成层级清晰、逻辑连贯的思维导图，帮助学生建立知识体系。"
                             "思维导图应包含中心主题、主要分支和子节点，以及节点间的关联关系。",
            llm_service=llm_service,
        )
        self.model_gateway = model_gateway

    def generate_mindmap(self, profile, request: str) -> MindMapResource:
        """生成个性化思维导图"""
        profile_context = self._format_profile_context(profile)

        system_prompt = self.get_system_prompt() + f"""
        基于以下学生画像，针对学生的学习需求生成知识思维导图。
        {profile_context}

        请返回JSON格式（不要包含```标记），包含以下字段：
        {{
            "central_topic": "中心主题",
            "nodes": [
                {{"id": "1", "label": "节点名称", "parent_id": null, "description": "描述", "level": 0}},
                {{"id": "2", "label": "子节点", "parent_id": "1", "description": "描述", "level": 1}}
            ],
            "connections": [
                {{"from": "1", "to": "2", "label": "关联说明"}}
            ]
        }}
        节点应不少于6个，层级不少于3级。
        """

        backend = self.model_gateway.get() if self.model_gateway else self.llm
        response = backend.chat(system_prompt, request)
        data = safe_json_parse(response) or {}

        resource = MindMapResource(
            resource_id=generate_id("mm"),
            title=data.get("central_topic", "知识点思维导图"),
            content=data,
            tags=[data.get("central_topic", "")],
            course_name=request[:50],
            created_at=now_str(),
            student_id=profile.student_id,
        )

        logger.info(f"MindMap generated: {resource.resource_id}")
        return resource

    def process(self) -> Optional[AgentMessage]:
        for msg in self.mailbox:
            if msg.message_type == "request":
                profile = msg.content.get("profile") if isinstance(msg.content, dict) else None
                request = msg.content.get("request", "") if isinstance(msg.content, dict) else str(msg.content)
                if not profile:
                    return AgentMessage(sender=self.name, receiver=msg.sender,
                                        message_type="response", content=None)
                mm = self.generate_mindmap(profile, request)
                return AgentMessage(sender=self.name, receiver=msg.sender,
                                    message_type="response", content=mm)
        self.mailbox.clear()
        return None
