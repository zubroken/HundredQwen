from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict

from fastapi import HTTPException

from services.chat_history_service import ChatHistoryService
from services.chat_prompt_service import ChatPromptService
from services.database import DatabaseManager
from services.llm_service import LLMService
from services.model_gateway import ModelGateway

if TYPE_CHECKING:
    from agents.profile_agent import ProfileAgent

logger = logging.getLogger(__name__)

EFFORT_TEMPERATURE = {"low": 0.3, "high": 0.7, "max": 1.0}


class ChatService:
    def __init__(
        self,
        db: DatabaseManager,
        llm_service: LLMService,
        profile_agent: "ProfileAgent",
        chat_history_service: ChatHistoryService,
        chat_prompt_service: ChatPromptService,
        model_gateway: ModelGateway | None = None,
    ):
        self.db = db
        self.llm_service = llm_service
        self.profile_agent = profile_agent
        self.chat_history_service = chat_history_service
        self.chat_prompt_service = chat_prompt_service
        self.model_gateway = model_gateway

    def chat(self, student_id: str, message: str,
             model: str = "deepseek", effort: str = "high") -> Dict[str, Any]:
        profile = self.db.get_student(student_id)
        if not profile:
            raise HTTPException(status_code=404, detail="学生画像未找到")

        kb_context = self.chat_prompt_service.build_kb_context(message)
        hist_context = self.chat_history_service.build_context(student_id)
        system_prompt = self.chat_prompt_service.build_system_prompt(
            profile,
            hist_context,
            kb_context,
        )

        backend = self.model_gateway.get(model) if self.model_gateway else self.llm_service
        temperature = EFFORT_TEMPERATURE.get(effort, 0.7)
        reply = backend.chat(system_prompt, message, temperature=temperature)
        self.chat_history_service.append_turn(student_id, message, reply)

        updated_profile = None
        try:
            dialogue = [{"role": "user", "content": message}]
            updated_profile = self.profile_agent.update_profile(profile, dialogue)
            self.db.save_profile(updated_profile)
        except Exception as exc:
            logger.warning(f"画像更新失败，使用原始画像继续: {exc}")

        return {
            "reply": reply,
            "profile": (updated_profile or profile).to_public_dict(),
        }
