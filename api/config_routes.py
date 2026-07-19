from __future__ import annotations

from fastapi import FastAPI

from api.schemas import LLMConfigRequest
from services.app_services import AppServices


def register_config_routes(app: FastAPI, services: AppServices) -> None:
    @app.get("/api/config/llm/status")
    async def get_model_status():
        return services.get_model_gateway_status()

    @app.put("/api/config/llm")
    async def update_llm_config(config: LLMConfigRequest):
        return services.update_llm_config(
            api_key=config.api_key,
            model=config.model,
            base_url=config.base_url,
        )
