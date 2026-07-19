"""
工具函数
"""
import uuid
import json
from datetime import datetime
from typing import Optional


def generate_id(prefix: str = "") -> str:
    """生成唯一ID"""
    uid = uuid.uuid4().hex[:12]
    return f"{prefix}_{uid}" if prefix else uid


def now_str() -> str:
    """当前时间字符串"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_len: int = 500) -> str:
    """截断文本"""
    return text[:max_len] + "..." if len(text) > max_len else text


def safe_json_parse(text: str) -> Optional[dict]:
    """安全解析JSON，支持从markdown代码块提取"""
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 尝试提取 ```json ... ``` 块
    if "```json" in text:
        try:
            block = text.split("```json")[1].split("```")[0].strip()
            return json.loads(block)
        except (IndexError, json.JSONDecodeError):
            pass
    if "```" in text:
        try:
            block = text.split("```")[1].split("```")[0].strip()
            return json.loads(block)
        except (IndexError, json.JSONDecodeError):
            pass
    return None
