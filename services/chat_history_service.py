from __future__ import annotations

import json
import logging
from typing import Dict, List

from settings import CHAT_HISTORY_DIR

logger = logging.getLogger(__name__)


MAX_CACHED_HISTORIES = 100  # 最多缓存 100 个学生的聊天记录


class ChatHistoryService:
    def __init__(self):
        self._chat_history: Dict[str, List[dict]] = {}
        self._access_order: list[str] = []  # LRU 淘汰队列

    def get_history(self, student_id: str) -> List[dict]:
        if student_id not in self._chat_history:
            self._chat_history[student_id] = self._load_chat_history(student_id)
            self._access_order.append(student_id)
        else:
            # 刷新 LRU 访问顺序
            self._access_order.remove(student_id)
            self._access_order.append(student_id)
        # LRU 淘汰：超过上限时移除最旧的
        while len(self._access_order) > MAX_CACHED_HISTORIES:
            oldest = self._access_order.pop(0)
            if oldest in self._chat_history:
                del self._chat_history[oldest]
        return self._chat_history[student_id]

    def build_context(self, student_id: str) -> str:
        hist = self.get_history(student_id)
        if not hist:
            return ""

        recent = hist[-6:]
        older = hist[:-6]
        lines = []
        for item in older:
            role = "学生" if item["role"] == "user" else "AI"
            lines.append(f"{role}: {item['content'][:200]}")
        for item in recent:
            role = "学生" if item["role"] == "user" else "AI"
            lines.append(f"{role}: {item['content']}")
        return "\n【近期对话记录】\n" + "\n".join(lines) + "\n请结合对话历史理解上下文，回答时保持连贯。"

    def append_turn(self, student_id: str, user_message: str, assistant_reply: str) -> None:
        hist = self.get_history(student_id)
        hist.append({"role": "user", "content": user_message})
        hist.append({"role": "assistant", "content": assistant_reply})
        self._save_chat_history(student_id, hist)

    def _load_chat_history(self, student_id: str) -> List[dict]:
        try:
            path = CHAT_HISTORY_DIR / f"{student_id}.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as exc:
            logger.warning(f"加载聊天历史失败 {student_id}: {exc}")
        return []

    def _save_chat_history(self, student_id: str, history: List[dict]) -> None:
        try:
            CHAT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
            path = CHAT_HISTORY_DIR / f"{student_id}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(history[-100:], f, ensure_ascii=False)
        except Exception as exc:
            logger.warning(f"保存聊天历史失败 {student_id}: {exc}")
