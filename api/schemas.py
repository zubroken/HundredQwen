from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ChatRequest(BaseModel):
    student_id: Optional[str] = ""
    message: str = Field(..., min_length=1, max_length=20000)
    course_name: str = "人工智能"


class ProfileResponse(BaseModel):
    student_id: str
    profile: dict
    message: str


class LLMConfigRequest(BaseModel):
    api_key: str = ""
    model: str = Field(default="deepseek-chat", min_length=1, max_length=100)
    base_url: str = ""


class LoginRequest(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class UpdateProfileRequest(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    updates: dict


class RegisterRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)
    major: str = "人工智能"


class ChatSimpleRequest(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    message: str = Field(..., min_length=1, max_length=20000)
    model: str = "deepseek"
    effort: str = "high"  # low / high / max


class ExerciseGenerateRequest(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    question_type: str = "choice"
    count: int = Field(default=5, ge=1, le=50)
    course_name: str = "人工智能"


class ZhiwenCreateRequest(BaseModel):
    query: str
    theme: str = "auto"
    detail_level: str = "standard"
    page_count: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def apply_legacy_page_count(cls, data):
        if not isinstance(data, dict):
            return data

        if "detail_level" in data:
            return data

        page_count = data.get("page_count")
        if not isinstance(page_count, int):
            return data

        if page_count <= 4:
            data["detail_level"] = "brief"
        elif page_count <= 7:
            data["detail_level"] = "standard"
        else:
            data["detail_level"] = "detailed"
        return data


class ZhiwenProgressRequest(BaseModel):
    sid: str


class KnowledgeSearchRequest(BaseModel):
    query: str
    type_filter: str = "all"
    doc_id: str = ""
    include_arxiv: bool = False


class DocumentGenerateRequest(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50)
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty: str = "intermediate"   # beginner / intermediate / advanced
    detail_level: str = "standard"     # brief / standard / detailed
    course_name: str = "人工智能"


class KnowledgeExportRequest(BaseModel):
    entry_id: str
    title: str = ""
    text: str = ""
    full_text: str = ""
    source: str = ""
    authors: list = []
    published: str = ""
    keywords: list = []
