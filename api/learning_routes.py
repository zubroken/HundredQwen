from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File

from api.schemas import ChatSimpleRequest, DocumentGenerateRequest, ExerciseGenerateRequest
from services.app_services import AppServices


def register_learning_routes(app: FastAPI, services: AppServices) -> None:
    @app.get("/api/study-time/{student_id}")
    async def get_study_time(student_id: str):
        return services.study_time_service.get_summary(student_id)

    @app.post("/api/study-time/{student_id}/start")
    async def start_study_time(student_id: str):
        try:
            return services.study_time_service.start(student_id)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/study-time/{student_id}/pause")
    async def pause_study_time(student_id: str):
        try:
            return services.study_time_service.pause(student_id)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/study-time/{student_id}/end")
    async def end_study_time(student_id: str):
        try:
            return services.study_time_service.end(student_id)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.post("/api/speech/recognize")
    async def speech_recognize(audio: UploadFile = File(...)):
        """语音识别：接收浏览器录音，返回识别文本"""
        try:
            audio_bytes = await audio.read()
            text = services.speech_service.recognize(audio_bytes)
            return {"text": text}
        except RuntimeError as e:
            raise HTTPException(status_code=503, detail=str(e))
        except TimeoutError:
            raise HTTPException(status_code=408, detail="语音识别超时（超过60秒）")

    @app.post("/api/chat-simple")
    async def chat_simple(req: ChatSimpleRequest):
        return services.chat_service.chat(req.student_id, req.message, req.model, req.effort)

    @app.post("/api/exercise/generate")
    async def generate_exercise(req: ExerciseGenerateRequest):
        return services.exercise_service.generate(
            req.student_id,
            req.question_type,
            req.count,
            req.course_name,
        )

    @app.post("/api/document/generate")
    async def generate_document(req: DocumentGenerateRequest):
        return services.document_service.generate(
            req.student_id,
            req.topic,
            req.difficulty,
            req.detail_level,
            req.course_name,
        )

    @app.get("/api/resources/{student_id}")
    async def get_resources(student_id: str, resource_type: Optional[str] = None):
        return services.resource_service.list_resources(student_id, resource_type)

    @app.get("/api/paths/{student_id}")
    async def get_paths(student_id: str):
        return services.resource_service.list_paths(student_id)
