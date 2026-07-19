"""
[v3.0] 编排器智能体 —— 多智能体系统的核心协调者
旧版全资源生成分发逻辑已注释，agent_map 保留以备后续复用。
负责任务分发、调度和结果整合
"""
from __future__ import annotations
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from agents.base_agent import BaseAgent, AgentMessage
from models.profile import StudentProfile
from models.resources import (Resource, ResourceType, LearningPath,
                                ResourceDB)
from services.llm_service import LLMService
from utils.helpers import generate_id, now_str

logger = logging.getLogger(__name__)


class Orchestrator(BaseAgent):
    """
    编排器 —— 负责任务分解、智能体调度、结果整合
    系统核心协调者
    """

    def __init__(self, llm_service: Optional[LLMService] = None):
        super().__init__(
            name="Orchestrator",
            role_description="你是多智能体学习系统的核心编排器。你负责任务分析、拆解、分发给合适的智能体，"
                             "并整合各智能体的输出结果。你需要理解学生的需求，协调各个专业智能体协同工作，"
                             "确保生成的个性化学习资源高质量且相互关联。",
            llm_service=llm_service,
        )
        self.agents: Dict[str, BaseAgent] = {}
        self.resource_db = ResourceDB()

    def register_agent(self, agent: BaseAgent):
        """注册子智能体"""
        self.agents[agent.name] = agent
        logger.info(f"Agent registered: {agent.name}")

    def _dispatch_task(self, task_type: str, profile: StudentProfile,
                       request: str) -> Any:
        """分发任务到对应的智能体"""
        agent_map = {
            "profile": "ProfileAgent",
            "document": "DocumentAgent",
            "mindmap": "MindMapAgent",
            "exercise": "ExerciseAgent",
            "reading": "ReadingAgent",
            "code": "CodeExampleAgent",
            "path": "LearningPathAgent",
        }

        agent_name = agent_map.get(task_type)
        if not agent_name or agent_name not in self.agents:
            logger.warning(f"No agent found for task type: {task_type}")
            return None

        agent = self.agents[agent_name]
        msg = self.send(agent, "request", content={
            "profile": profile,
            "request": request,
            "task_type": task_type,
        })

        # 触发智能体处理
        response_msg = agent.process()
        if response_msg:
            logger.info(f"Agent {agent_name} completed task: {task_type}")
            return response_msg.content
        return None

    def process(self) -> Optional[AgentMessage]:
        """处理编排器自己的消息"""
        for msg in self.mailbox:
            if msg.message_type == "orchestrate":
                logger.warning("orchestrate 消息类型已废弃")
                return AgentMessage(
                    sender=self.name,
                    receiver="__main__",
                    message_type="result",
                    content={},
                )
        self.mailbox.clear()
        return None
