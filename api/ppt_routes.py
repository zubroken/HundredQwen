from __future__ import annotations

from fastapi import FastAPI

from api.schemas import ZhiwenCreateRequest, ZhiwenProgressRequest
from services.app_services import AppServices


def register_ppt_routes(app: FastAPI, services: AppServices) -> None:
    @app.get("/api/zhiwen/themes")
    async def get_zhiwen_themes():
        return services.ppt_service.list_themes()

    @app.post("/api/zhiwen/ppt/create")
    async def create_zhiwen_ppt(req: ZhiwenCreateRequest):
        return services.ppt_service.create_ppt(
            query=req.query,
            theme=req.theme,
            detail_level=req.detail_level,
        )

    @app.post("/api/zhiwen/ppt/progress")
    async def get_zhiwen_progress(req: ZhiwenProgressRequest):
        return services.ppt_service.get_progress(req.sid)
