from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException

from services.database import DatabaseManager
from services.knowledge_base import KnowledgeBase


class ExerciseService:
    def __init__(self, db: DatabaseManager, knowledge_base: KnowledgeBase, exercise_agent: Any):
        self.db = db
        self.knowledge_base = knowledge_base
        self.exercise_agent = exercise_agent

    def generate(self, student_id: str, question_type: str, count: int, course_name: str) -> Dict[str, Any]:
        profile = self.db.get_student(student_id)
        if not profile:
            raise HTTPException(status_code=404, detail="学生画像未找到")

        type_names = {
            "choice": "选择题",
            "fill_blank": "填空题",
            "short_answer": "简答题",
        }
        type_name = type_names.get(question_type, "练习题")

        # 基于学生薄弱知识点或课程名检索教材内容
        retrieval_query = " ".join(profile.weak_points[:3]) if profile.weak_points else course_name
        kb_context = ""
        chunks = self.knowledge_base.retrieve(retrieval_query, top_k=3)
        if chunks:
            kb_context = "\n【参考资料（请基于以下教材内容出题）】\n" + self.knowledge_base.format_context(chunks)

        request_text = f"课程：{course_name}。请生成{count}道{type_name}，难度递进，只出{type_name}题型。{kb_context}"

        ex_resource = self.exercise_agent.generate_exercises(profile, request_text)
        return {
            "questions": ex_resource.content.get("questions", []),
            "total_score": ex_resource.content.get("total_score", 100),
            "estimated_time_minutes": ex_resource.content.get("estimated_time_minutes", 10),
        }
