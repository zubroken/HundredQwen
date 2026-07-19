from __future__ import annotations

from fastapi import FastAPI

from api.schemas import ChatRequest, LoginRequest, ProfileResponse, RegisterRequest, UpdateProfileRequest
from services.app_services import AppServices


def register_account_routes(app: FastAPI, services: AppServices) -> None:
    @app.post("/api/login")
    async def login(req: LoginRequest):
        return services.account_service.login(req.student_id, req.password)

    @app.post("/api/register")
    async def register(req: RegisterRequest):
        return services.account_service.register(req.nickname, req.major)

    @app.put("/api/profile/update")
    async def update_profile(req: UpdateProfileRequest):
        return services.account_service.update_profile(req.student_id, req.updates)

    @app.delete("/api/account/{student_id}")
    async def delete_account(student_id: str):
        return services.account_service.delete_account(student_id)

    @app.post("/api/chat", response_model=ProfileResponse)
    async def chat_start(req: ChatRequest):
        return ProfileResponse(
            **services.account_service.build_profile_from_chat(
                req.student_id,
                req.message,
                req.course_name,
            )
        )

    @app.get("/api/profile/{student_id}")
    async def get_profile(student_id: str):
        return services.account_service.get_profile(student_id)
