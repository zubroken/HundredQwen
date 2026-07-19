from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.app_services import AppServices


class SkillTreeExerciseRequest(BaseModel):
    student_id: str = Field(default="stu_001", min_length=1, max_length=50)
    chapter_id: int = Field(..., ge=1, le=7)
    node_id: str = Field(..., min_length=1)
    level: str = Field(default="l3", pattern=r"^l[123]$")
    exercise_index: int = Field(default=0, ge=0, le=4)


class SkillTreeSubmitRequest(BaseModel):
    student_id: str = Field(default="stu_001", min_length=1, max_length=50)
    chapter_id: int = Field(..., ge=1, le=7)
    node_id: str = Field(..., min_length=1)
    level: str = Field(default="l3", pattern=r"^l[123]$")
    user_answer: str = Field(..., min_length=1)
    exercise_data: dict = Field(default_factory=dict)
    exercise_index: int = Field(default=0, ge=0, le=4)


def register_skill_tree_routes(app: FastAPI, services: AppServices) -> None:
    @app.get("/api/skill-tree")
    async def get_skill_tree(student_id: str = "stu_001"):
        return services.skill_tree_service.build_tree_response(student_id)

    @app.get("/api/skill-tree/chapter/{chapter_id}")
    async def get_chapter_detail(chapter_id: int, student_id: str = "stu_001"):
        try:
            return services.skill_tree_service.get_chapter_detail(student_id, chapter_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.post("/api/skill-tree/exercise/generate")
    async def generate_exercise(req: SkillTreeExerciseRequest):
        try:
            return services.skill_tree_service.generate_exercise(
                req.student_id, req.chapter_id, req.node_id, req.level,
                exercise_index=req.exercise_index
            )
        except (ValueError, RuntimeError) as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/skill-tree/exercise/submit")
    async def submit_exercise(req: SkillTreeSubmitRequest):
        try:
            return services.skill_tree_service.submit_answer(
                req.student_id, req.chapter_id, req.node_id, req.level,
                req.user_answer, req.exercise_data,
                exercise_index=req.exercise_index
            )
        except (ValueError, RuntimeError) as e:
            raise HTTPException(status_code=400, detail=str(e))
