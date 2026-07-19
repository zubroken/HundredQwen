"""
FastAPI application assembly entrypoint.
"""
from __future__ import annotations

from typing import Optional

from fastapi import FastAPI

from api.account_routes import register_account_routes
from api.config_routes import register_config_routes
from api.generation_routes import register_generation_routes
from api.home_routes import register_home_routes
from api.knowledge_routes import register_knowledge_routes
from api.learning_routes import register_learning_routes
from api.ppt_routes import register_ppt_routes
from api.skill_tree_routes import register_skill_tree_routes
from services.app_services import build_app_services
from services.llm_service import LLMConfig
from settings import VERSION


def create_app(llm_config: Optional[LLMConfig] = None) -> FastAPI:
    app = FastAPI(
        title=f"百问即查 v{VERSION} - AI 智能学习助手",
        version=VERSION,
    )
    services = build_app_services(llm_config or LLMConfig())

    register_home_routes(app)
    register_account_routes(app, services)
    register_learning_routes(app, services)
    register_generation_routes(app, services)
    register_config_routes(app, services)
    register_ppt_routes(app, services)
    register_knowledge_routes(app, services)
    register_skill_tree_routes(app, services)

    return app
