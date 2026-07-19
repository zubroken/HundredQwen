from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import HTTPException

from models.profile import StudentProfile
from services.database import DatabaseManager
from utils.helpers import generate_id

logger = logging.getLogger(__name__)


class AccountService:
    def __init__(self, db: DatabaseManager, profile_agent: Any):
        self.db = db
        self.profile_agent = profile_agent

    def login(self, student_id: str, password: str) -> Dict[str, Any]:
        profile = self.db.verify_login(student_id, password)
        if not profile:
            existing = self.db.get_student(student_id)
            if not existing:
                raise HTTPException(status_code=404, detail="学号不存在")
            raise HTTPException(status_code=401, detail="密码错误")
        return {
            "success": True,
            "student_id": profile.student_id,
            "profile": profile.to_public_dict(),
        }

    def register(self, nickname: str, major: str = "人工智能") -> Dict[str, Any]:
        # 检查重名
        all_students = self.db.list_all()
        for s in all_students:
            if s.name == nickname:
                raise HTTPException(status_code=409, detail="该昵称已被注册")
        student_id = generate_id("stu")
        # 确保 ID 不冲突（理论上极低概率）
        while self.db.get_student(student_id):
            student_id = generate_id("stu")
        profile = StudentProfile(
            student_id=student_id,
            password="1",
            name=nickname,
            school="",
            major=major,
            grade="大一",
            knowledge_base="对人工智能有浓厚兴趣，正在入门学习",
            cognitive_style="逻辑型",
            weak_points=[],
            learning_goals=["系统学习人工智能核心知识"],
            learning_pace="中",
            interest_topics=["人工智能", "机器学习", "深度学习"],
            preferred_resource_types=["概念图解", "代码案例"],
            programming_exp="了解Python基础",
            avatar="avatar-1",
        )
        self.db.save_profile(profile)
        return {"success": True, "student_id": student_id}

    def update_profile(self, student_id: str, updates: dict) -> Dict[str, Any]:
        profile = self.db.get_student(student_id)
        if not profile:
            raise HTTPException(status_code=404, detail="学号不存在")

        self.db.update_profile(student_id, updates)
        # 仅读一次：重新加载更新后的画像
        profile = self.db.get_student(student_id)

        try:
            profile = self.profile_agent.build_profile_from_dialogue([
                {
                    "role": "system",
                    "content": (
                        f"学生主动提供了以下画像信息：知识基础={profile.knowledge_base}, "
                        f"认知风格={profile.cognitive_style}, 薄弱点={profile.weak_points}, "
                        f"学习目标={profile.learning_goals}, 学习节奏={profile.learning_pace}, "
                        f"兴趣={profile.interest_topics}, 偏好资源={profile.preferred_resource_types}, "
                        f"编程经验={profile.programming_exp}。请基于这些信息完善学生画像，补全任何缺失的维度。"
                    ),
                }
            ])
            profile.student_id = student_id
            profile.name = updates.get("name") or profile.name
            profile.school = updates.get("school") or profile.school
            profile.major = "人工智能"
            self.db.save_profile(profile)
        except Exception as exc:
            logger.warning(f"画像 LLM 重建失败，回退到数据库画像: {exc}")

        return {
            "success": True,
            "message": "画像已更新",
            "profile": profile.to_public_dict(),
        }

    def delete_account(self, student_id: str) -> Dict[str, Any]:
        deleted = self.db.delete_student(student_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="学号不存在")
        return {"success": True, "message": f"账号 {student_id} 已注销"}

    def get_profile(self, student_id: str) -> Dict[str, Any]:
        profile = self.db.get_student(student_id)
        if not profile:
            raise HTTPException(status_code=404, detail="学生画像未找到")
        return profile.to_public_dict()

    def build_profile_from_chat(self, student_id: str, message: str, course_name: str) -> Dict[str, Any]:
        dialogue = [{"role": "user", "content": message}]
        if student_id:
            existing = self.db.get_student(student_id)
            if existing:
                profile = self.profile_agent.update_profile(existing, dialogue)
            else:
                profile = self.profile_agent.build_profile_from_dialogue(dialogue)
                profile.student_id = student_id
                profile.password = "1"
        else:
            profile = self.profile_agent.build_profile_from_dialogue(dialogue)
            profile.password = "1"

        profile.major = profile.major or course_name
        self.db.save_profile(profile)
        return {
            "student_id": profile.student_id,
            "profile": profile.to_public_dict(),
            "message": f"已为您构建学习画像！您的学号是：{profile.student_id}。",
        }
