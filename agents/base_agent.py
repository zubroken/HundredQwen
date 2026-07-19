"""
智能体基类 —— 所有智能体继承此类
定义了智能体的生命周期和通信接口
"""
from __future__ import annotations
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

from services.llm_service import LLMService, LLMConfig
from models.profile import StudentProfile
from models.resources import Resource

logger = logging.getLogger(__name__)


@dataclass
class AgentMessage:
    """智能体间通信消息"""
    sender: str
    receiver: str
    message_type: str       # request / response / notify
    content: Any = None
    metadata: Dict = field(default_factory=dict)


class BaseAgent:
    """
    智能体基类
    每个智能体有明确的角色定义和职责范围
    """

    def __init__(self, name: str, role_description: str,
                 llm_service: Optional[LLMService] = None):
        self.name = name
        self.role_description = role_description
        self.llm = llm_service or LLMService()
        self.mailbox: List[AgentMessage] = []

    def receive(self, message: AgentMessage):
        """接收来自其他智能体的消息"""
        self.mailbox.append(message)
        logger.debug(f"[{self.name}] Received message from {message.sender}: {message.message_type}")

    def send(self, receiver: "BaseAgent", message_type: str,
             content: Any = None, metadata: Optional[Dict] = None) -> AgentMessage:
        """向指定智能体发送消息"""
        msg = AgentMessage(
            sender=self.name,
            receiver=receiver.name,
            message_type=message_type,
            content=content,
            metadata=metadata or {},
        )
        receiver.receive(msg)
        return msg

    def process(self) -> Optional[AgentMessage]:
        """
        处理邮箱中的消息 —— 子类实现具体逻辑
        返回可选的响应消息
        """
        raise NotImplementedError

    def get_system_prompt(self) -> str:
        """获取该智能体的系统提示词"""
        return f"""你是{self.name}。
角色描述：{self.role_description}
请根据你的角色职责，使用中文回复，为用户提供专业的服务。"""

    def _format_profile_context(self, profile: Optional[StudentProfile]) -> str:
        """格式化学生画像上下文"""
        if not profile:
            return "暂无学生画像信息。"
        context = f"""学生信息：
- 专业：{profile.major}
- 年级：{profile.grade}
- 知识基础：{profile.knowledge_base}
- 认知风格：{profile.cognitive_style}
- 薄弱知识点：{', '.join(profile.weak_points) if profile.weak_points else '暂无'}
- 学习目标：{', '.join(profile.learning_goals) if profile.learning_goals else '暂无'}
- 学习进度偏好：{profile.learning_pace}
- 兴趣方向：{', '.join(profile.interest_topics) if profile.interest_topics else '暂无'}
- 偏好资源类型：{', '.join(profile.preferred_resource_types) if profile.preferred_resource_types else '暂无'}
- 编程经验：{profile.programming_exp}"""
        return context
