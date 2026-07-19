"""
资源模型 —— 5种以上不同类型的个性化学习资源
"""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from settings import RESOURCES_PATH


class ResourceType(str, Enum):
    DOCUMENT = "document"           # 专业课程讲解文档
    MINDMAP = "mindmap"             # 知识点思维导图
    EXERCISE = "exercise"           # 练习题目
    READING = "reading"             # 拓展阅读材料
    CODE_EXAMPLE = "code_example"   # 代码实操案例


class ExerciseType(str, Enum):
    CHOICE = "choice"               # 选择题
    FILL_BLANK = "fill_blank"       # 填空题
    SHORT_ANSWER = "short_answer"   # 简答题
    CODING = "coding"               # 编程题
    TRUE_FALSE = "true_false"       # 判断题


@dataclass
class Resource:
    """通用资源基类"""
    resource_id: str = ""
    title: str = ""
    resource_type: str = ResourceType.DOCUMENT
    content: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    difficulty: str = "intermediate"  # beginner / intermediate / advanced
    course_name: str = ""
    created_at: str = ""
    student_id: str = ""  # 关联的学生

    citations: List[Dict[str, Any]] = field(default_factory=list)
    evidence_level: str = "unknown"
    fallback: bool = False

    def to_dict(self) -> dict:
        data = asdict(self)
        if isinstance(data.get("resource_type"), Enum):
            data["resource_type"] = data["resource_type"].value
        if not self.citations:
            data.pop("citations", None)
        if self.evidence_level == "unknown":
            data.pop("evidence_level", None)
        if not self.fallback:
            data.pop("fallback", None)
        return data

    @classmethod
    def from_dict(cls, d: dict) -> "Resource":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class DocumentResource(Resource):
    """课程讲解文档"""
    def __init__(self, **kwargs):
        kwargs.setdefault("resource_type", ResourceType.DOCUMENT)
        super().__init__(**kwargs)
        self.content.setdefault("sections", [])
        self.content.setdefault("summary", "")
        self.content.setdefault("prerequisites", [])
        self.content.setdefault("key_concepts", [])
        self.content.setdefault("references", [])


@dataclass
class MindMapResource(Resource):
    """思维导图"""
    def __init__(self, **kwargs):
        kwargs.setdefault("resource_type", ResourceType.MINDMAP)
        super().__init__(**kwargs)
        self.content.setdefault("central_topic", "")
        self.content.setdefault("nodes", [])   # list of {id, label, parent_id, description, level}
        self.content.setdefault("connections", [])  # list of {from, to, label}


@dataclass
class ExerciseResource(Resource):
    """练习题"""
    def __init__(self, **kwargs):
        kwargs.setdefault("resource_type", ResourceType.EXERCISE)
        super().__init__(**kwargs)
        self.content.setdefault("exercise_type", ExerciseType.CHOICE)
        self.content.setdefault("questions", [])  # list of {stem, options[], answer, explanation, difficulty}
        self.content.setdefault("total_score", 0)
        self.content.setdefault("estimated_time_minutes", 0)


@dataclass
class ReadingResource(Resource):
    """拓展阅读材料"""
    def __init__(self, **kwargs):
        kwargs.setdefault("resource_type", ResourceType.READING)
        super().__init__(**kwargs)
        self.content.setdefault("materials", [])  # list of {title, url, type, summary, relevance}
        self.content.setdefault("reading_guide", "")
        self.content.setdefault("discussion_points", [])


@dataclass
class CodeResource(Resource):
    """代码实操案例"""
    def __init__(self, **kwargs):
        kwargs.setdefault("resource_type", ResourceType.CODE_EXAMPLE)
        super().__init__(**kwargs)
        self.content.setdefault("language", "")
        self.content.setdefault("code", "")
        self.content.setdefault("explanation", "")
        self.content.setdefault("setup_steps", [])
        self.content.setdefault("expected_output", "")
        self.content.setdefault("challenges", [])
        self.content.setdefault("hints", [])


@dataclass
class PathNode:
    """学习路径中的一个节点"""
    node_id: str = ""
    title: str = ""
    description: str = ""
    resource_ids: List[str] = field(default_factory=list)
    estimated_hours: float = 1.0
    prerequisites: List[str] = field(default_factory=list)
    status: str = "pending"  # pending / in_progress / completed
    order: int = 0


@dataclass
class LearningPath:
    """个性化学习路径"""
    path_id: str = ""
    student_id: str = ""
    course_name: str = ""
    title: str = ""
    description: str = ""
    nodes: List[PathNode] = field(default_factory=list)
    total_estimated_hours: float = 0.0
    difficulty: str = "intermediate"
    created_at: str = ""
    updated_at: str = ""
    status: str = "active"  # active / completed / paused

    def to_dict(self) -> dict:
        return {
            "path_id": self.path_id,
            "student_id": self.student_id,
            "course_name": self.course_name,
            "title": self.title,
            "description": self.description,
            "nodes": [asdict(n) for n in self.nodes],
            "total_estimated_hours": self.total_estimated_hours,
            "difficulty": self.difficulty,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "LearningPath":
        data = dict(d)
        nodes = [PathNode(**n) for n in data.pop("nodes", [])]
        lp = cls(**data)
        lp.nodes = nodes
        return lp


@dataclass
class ResourceBundle:
    bundle_id: str
    student_id: str
    topic: str
    course_name: str
    resource_ids: List[str]
    path_id: Optional[str]
    citations: List[Dict[str, Any]]
    safety: Dict[str, Any]
    status: str = "completed"
    created_at: str = ""
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ResourceBundle":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class ResourceDB:
    """资源存储"""

    def __init__(self, path: Optional[str] = None):
        self.path = Path(path) if path else RESOURCES_PATH

    def _load_all(self) -> dict:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data.setdefault("resources", [])
        data.setdefault("learning_paths", [])
        data.setdefault("resource_bundles", [])
        return data

    def _save_all(self, data: dict):
        import os
        os.makedirs(self.path.parent, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_resource(self, resource: Resource):
        data = self._load_all()
        # 替换同ID或追加
        existing = [i for i, r in enumerate(data["resources"]) if r.get("resource_id") == resource.resource_id]
        existing = [i for i, r in enumerate(data["resources"]) if r.get("resource_id") == resource.resource_id]
        if existing:
            data["resources"][existing[0]] = resource.to_dict()
        else:
            data["resources"].append(resource.to_dict())
        self._save_all(data)

    def save_path(self, path: LearningPath):
        data = self._load_all()
        existing = [i for i, p in enumerate(data["learning_paths"]) if p.get("path_id") == path.path_id]
        if existing:
            data["learning_paths"][existing[0]] = path.to_dict()
        else:
            data["learning_paths"].append(path.to_dict())
        self._save_all(data)

    def get_resources_by_student(self, student_id: str, resource_type: Optional[str] = None) -> List[Resource]:
        data = self._load_all()
        results = []
        for r in data["resources"]:
            if r.get("student_id") == student_id:
                if resource_type and r.get("resource_type") != resource_type:
                    continue
                results.append(Resource.from_dict(r))
        return results

    def get_paths_by_student(self, student_id: str) -> List[LearningPath]:
        data = self._load_all()
        return [LearningPath.from_dict(p) for p in data["learning_paths"] if p.get("student_id") == student_id]

    def save_bundle(self, bundle: ResourceBundle) -> None:
        data = self._load_all()
        existing = [
            i for i, b in enumerate(data["resource_bundles"])
            if b.get("bundle_id") == bundle.bundle_id
        ]
        if existing:
            data["resource_bundles"][existing[0]] = bundle.to_dict()
        else:
            data["resource_bundles"].append(bundle.to_dict())
        self._save_all(data)

    def get_bundles_by_student(self, student_id: str) -> List[dict]:
        data = self._load_all()
        return [
            b for b in data["resource_bundles"]
            if b.get("student_id") == student_id
        ]

    def get_path_by_id(self, path_id: str) -> Optional[LearningPath]:
        data = self._load_all()
        for item in data["learning_paths"]:
            if item.get("path_id") == path_id:
                return LearningPath.from_dict(item)
        return None
