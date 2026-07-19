"""
学习路径规划智能体 - 生成个性化学习路径
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from agents.base_agent import AgentMessage, BaseAgent
from models.resources import LearningPath, PathNode
from services.llm_service import LLMService
from services.model_gateway import ModelGateway
from utils.helpers import generate_id, now_str, safe_json_parse

logger = logging.getLogger(__name__)


class LearningPathAgent(BaseAgent):
    """
    学习路径规划智能体 - 根据学生画像和生成资源，规划结构化学习路径
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        model_gateway: Optional[ModelGateway] = None,
    ):
        super().__init__(
            name="LearningPathAgent",
            role_description="你是学习路径规划专家。根据学生的专业背景、知识基础、学习目标和认知风格，"
            "结合已有学习资源，为学生规划科学、动态的个性化学习路径。"
            "学习路径应循序渐进、重点突出，合理安排学习时间和顺序，"
            "确保学生能够高效达成学习目标。",
            llm_service=llm_service,
        )
        self.model_gateway = model_gateway

    def generate_path(self, profile, resources: Dict[str, Any] | None = None) -> LearningPath:
        """生成个性化学习路径"""
        resource_ids = {}
        if resources:
            for resource_type, resource in resources.items():
                if hasattr(resource, "resource_id"):
                    resource_ids[resource_type] = resource.resource_id

        profile_context = self._format_profile_context(profile)
        system_prompt = self.get_system_prompt() + f"""
        基于以下学生画像，规划一个个性化的学习路径。
        {profile_context}

        请返回 JSON 格式（不要包含 ``` 标记），包含以下字段：
        {{
            "title": "学习路径标题",
            "description": "路径描述",
            "nodes": [
                {{
                    "order": 1,
                    "title": "阶段名称",
                    "description": "学习内容说明",
                    "estimated_hours": 2,
                    "prerequisites": []
                }}
            ],
            "total_estimated_hours": 2,
            "difficulty": "beginner/intermediate/advanced"
        }}
        学习路径应包含 3-8 个阶段，由浅入深。
        """

        backend = self.model_gateway.get() if self.model_gateway else self.llm
        response = backend.chat(system_prompt, f"学生需求：{profile.learning_goals}")
        data = safe_json_parse(response) or {}

        path = LearningPath(
            path_id=generate_id("path"),
            student_id=profile.student_id,
            title=data.get("title", "个性化学习路径"),
            description=data.get("description", ""),
            total_estimated_hours=data.get("total_estimated_hours", 0),
            difficulty=data.get("difficulty", "intermediate"),
            created_at=now_str(),
            updated_at=now_str(),
        )

        for index, node_data in enumerate(data.get("nodes", [])):
            node = PathNode(
                node_id=generate_id("node"),
                title=node_data.get("title", f"阶段{index + 1}"),
                description=node_data.get("description", ""),
                estimated_hours=node_data.get("estimated_hours", 1.0),
                prerequisites=node_data.get("prerequisites", []),
                status="pending",
                order=node_data.get("order", index + 1),
            )
            node.resource_ids = list(resource_ids.values())
            path.nodes.append(node)

        logger.info(f"Learning path generated: {path.path_id}")
        return path

    def process(self) -> Optional[AgentMessage]:
        for msg in self.mailbox:
            if msg.message_type == "request":
                profile = msg.content.get("profile") if isinstance(msg.content, dict) else None
                resources = msg.content.get("resources", {}) if isinstance(msg.content, dict) else {}

                if not profile:
                    return AgentMessage(
                        sender=self.name,
                        receiver=msg.sender,
                        message_type="response",
                        content=None,
                    )

                path = self.generate_path(profile, resources)
                return AgentMessage(
                    sender=self.name,
                    receiver=msg.sender,
                    message_type="response",
                    content=path,
                )
        self.mailbox.clear()
        return None
