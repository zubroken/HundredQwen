"""
学生画像模型 —— 包含不少于6个维度的动态学生画像
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional, List


@dataclass
class StudentProfile:
    """动态学生画像 —— 随学随新"""

    # ===== 基本信息 =====
    student_id: str = ""
    name: str = ""
    school: str = ""                    # 学校
    major: str = ""                     # 专业
    grade: str = ""                     # 年级

    # ===== 6+ 核心维度 =====
    knowledge_base: str = ""            # 维度1：知识基础（先修课程掌握程度等）
    cognitive_style: str = ""           # 维度2：认知风格（视觉型/听觉型/读写型/动觉型等）
    weak_points: List[str] = field(default_factory=list)   # 维度3：易错点/薄弱知识点
    learning_goals: List[str] = field(default_factory=list) # 维度4：学习目标
    learning_pace: str = ""             # 维度5：学习进度偏好（快/中/慢）
    interest_topics: List[str] = field(default_factory=list) # 维度6：兴趣方向
    preferred_resource_types: List[str] = field(default_factory=list)  # 维度7：偏好资源类型
    programming_exp: str = ""           # 维度8：编程经验水平
    avatar: str = "avatar-1"             # 头像编号 (avatar-1 ~ avatar-8)

    # ===== 元信息 =====
    created_at: str = ""
    updated_at: str = ""
    password: str = ""                    # 登录密码
    conversation_history: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_public_dict(self) -> dict:
        data = self.to_dict()
        data.pop("password", None)
        return data

    @classmethod
    def from_dict(cls, d: dict) -> "StudentProfile":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
