"""
课程文档生成服务 —— 调用 DocumentAgent 生成个性化课程讲解文档
"""
from __future__ import annotations
import logging
from typing import Optional

from agents.document_agent import DocumentAgent
from services.database import DatabaseManager
from services.knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)

DIFFICULTY_LABELS = {
    "beginner": "入门",
    "intermediate": "进阶",
    "advanced": "高级",
}
DETAIL_LABELS = {
    "brief": "精简（约2-3节核心要点）",
    "standard": "标准（约4-6节均衡展开）",
    "detailed": "详尽（约7-10节全面覆盖）",
}


class DocumentService:
    """课程文档生成服务"""

    def __init__(
        self,
        db: DatabaseManager,
        document_agent: DocumentAgent,
        knowledge_base: Optional[KnowledgeBase] = None,
    ):
        self.db = db
        self.agent = document_agent
        self.kb = knowledge_base

    def generate(
        self,
        student_id: str,
        topic: str,
        difficulty: str = "intermediate",
        detail_level: str = "standard",
        course_name: str = "人工智能",
    ) -> dict:
        """生成个性化课程讲解文档"""
        profile = self.db.get_student(student_id)
        if not profile:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail=f"学生 {student_id} 不存在")

        request_text = self._build_request(topic, difficulty, detail_level, course_name)
        doc = self.agent.generate_document(profile, request_text)

        # 补充元信息
        doc.difficulty = difficulty
        doc.course_name = course_name

        # 持久化到资源库
        try:
            self.agent.resource_db.save_resource(doc)
            logger.info(f"Document saved: {doc.resource_id}")
        except Exception as e:
            logger.warning(f"Failed to save document: {e}")

        return {
            "resource_id": doc.resource_id,
            "title": doc.title,
            "sections": doc.content.get("sections", []),
            "summary": doc.content.get("summary", ""),
            "prerequisites": doc.content.get("prerequisites", []),
            "key_concepts": doc.content.get("key_concepts", []),
            "references": doc.content.get("references", []),
            "difficulty": doc.difficulty,
            "difficulty_label": DIFFICULTY_LABELS.get(doc.difficulty, "进阶"),
            "detail_level": detail_level,
            "course_name": doc.course_name,
            "created_at": doc.created_at,
            "tags": doc.tags,
        }

    def _build_request(
        self,
        topic: str,
        difficulty: str,
        detail_level: str,
        course_name: str,
    ) -> str:
        """拼接发送给 LLM 的请求文本"""
        parts = [f"请为课程「{course_name}」生成一份关于「{topic}」的个性化讲解文档。"]

        diff_hint = {
            "beginner": "面向初学者，使用通俗易懂的语言，多用类比和图示化描述，避免复杂的数学公式。",
            "intermediate": "面向有一定基础的学习者，可以包含适度的公式推导和算法伪代码。",
            "advanced": "面向高级学习者，可以深入探讨数学原理、优化方法和前沿研究进展。",
        }
        parts.append(diff_hint.get(difficulty, diff_hint["intermediate"]))

        detail_hint = {
            "brief": "生成精简版文档，包含2-3个核心章节，每节约300-500字，重点突出最关键的概念。",
            "standard": "生成标准版文档，包含4-6个章节，每节约500-800字，概念讲解与实例并重。",
            "detailed": "生成详尽版文档，包含7-10个章节，每节约800-1200字，全面覆盖主题的各个方面，含丰富的案例和扩展阅读指引。",
        }
        parts.append(detail_hint.get(detail_level, detail_hint["standard"]))

        return " ".join(parts)
