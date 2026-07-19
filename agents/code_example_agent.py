"""
代码示例智能体 —— 生成代码实操案例
"""
from __future__ import annotations
import logging
from typing import Optional

from agents.base_agent import BaseAgent, AgentMessage
from models.resources import CodeResource
from services.llm_service import LLMService
from services.model_gateway import ModelGateway
from utils.helpers import generate_id, now_str, safe_json_parse

logger = logging.getLogger(__name__)


class CodeExampleAgent(BaseAgent):
    """
    代码智能体 —— 根据学生编程水平和学习目标生成代码实操案例
    包含完整代码、步骤说明、挑战任务
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        model_gateway: Optional[ModelGateway] = None,
    ):
        super().__init__(
            name="CodeExampleAgent",
            role_description="你是代码实操案例生成专家。擅长根据学生的编程水平和学习目标，"
                             "生成贴近实际应用的代码案例。每个案例应包含完整的可运行代码、"
                             "详细的代码解释、运行环境配置说明、预期输出、以及拓展挑战任务。"
                             "代码应遵循最佳实践，注释清晰。",
            llm_service=llm_service,
        )
        self.model_gateway = model_gateway

    def generate_code_example(self, profile, request: str) -> CodeResource:
        """生成个性化代码实操案例"""
        profile_context = self._format_profile_context(profile)

        system_prompt = self.get_system_prompt() + f"""
        基于以下学生画像，生成一个代码实操案例。
        {profile_context}
        学生编程经验：{profile.programming_exp}
        学生的兴趣方向：{', '.join(profile.interest_topics) if profile.interest_topics else '根据需求判断'}

        请返回JSON格式（不要包含```标记），包含以下字段：
        {{
            "title": "案例标题",
            "language": "编程语言",
            "code": "完整的可运行代码",
            "explanation": "代码详细讲解",
            "setup_steps": ["步骤1", "步骤2"],
            "expected_output": "预期输出结果",
            "challenges": ["挑战任务1", "挑战任务2"],
            "hints": ["提示1", "提示2"]
        }}
        代码应真实可用，与课程知识点紧密相关。
        """

        backend = self.model_gateway.get() if self.model_gateway else self.llm
        response = backend.chat(system_prompt, request)
        data = safe_json_parse(response) or {}

        resource = CodeResource(
            resource_id=generate_id("code"),
            title=data.get("title", "代码实操案例"),
            content=data,
            tags=[data.get("language", "Python")],
            course_name=request[:50],
            created_at=now_str(),
            student_id=profile.student_id,
        )

        logger.info(f"Code example generated: {resource.resource_id}")
        return resource

    def process(self) -> Optional[AgentMessage]:
        for msg in self.mailbox:
            if msg.message_type == "request":
                profile = msg.content.get("profile") if isinstance(msg.content, dict) else None
                request = msg.content.get("request", "") if isinstance(msg.content, dict) else str(msg.content)
                if not profile:
                    return AgentMessage(sender=self.name, receiver=msg.sender,
                                        message_type="response", content=None)
                code_example = self.generate_code_example(profile, request)
                return AgentMessage(sender=self.name, receiver=msg.sender,
                                    message_type="response", content=code_example)
        self.mailbox.clear()
        return None
