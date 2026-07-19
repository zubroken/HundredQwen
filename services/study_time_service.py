from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

from settings import DB_PATH


INITIAL_SECONDS = 26 * 60 * 60


class StudyTimeService:
    """管理用户手动开启的学习会话及周累计时长。"""

    def __init__(
        self,
        db_path: Path = DB_PATH,
        clock: Callable[[], datetime] | None = None,
        initial_seconds: int = INITIAL_SECONDS,
    ) -> None:
        self.db_path = Path(db_path)
        self.clock = clock or datetime.now
        self.initial_seconds = initial_seconds
        self._init_db()

    @contextmanager
    def _connection(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except BaseException:
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS study_time_accounts (
                    student_id TEXT PRIMARY KEY,
                    initial_seconds INTEGER NOT NULL DEFAULT 0,
                    initial_week_start TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS study_time_sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    ended_at TEXT,
                    duration_seconds INTEGER NOT NULL DEFAULT 0
                )
                """
            )

    def _now(self) -> datetime:
        return self.clock()

    @staticmethod
    def _week_start(value: datetime) -> datetime:
        return datetime(value.year, value.month, value.day) - timedelta(days=value.weekday())

    @staticmethod
    def _serialize(value: datetime) -> str:
        return value.isoformat(timespec="seconds")

    def _ensure_account(self, conn: sqlite3.Connection, student_id: str, now: datetime) -> None:
        week_start = self._week_start(now)
        conn.execute(
            """
            INSERT OR IGNORE INTO study_time_accounts
                (student_id, initial_seconds, initial_week_start, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, self.initial_seconds, week_start.date().isoformat(), self._serialize(now)),
        )

    def start(self, student_id: str) -> dict:
        now = self._now()
        with self._connection() as conn:
            self._ensure_account(conn, student_id, now)
            active = conn.execute(
                "SELECT * FROM study_time_sessions WHERE student_id=? AND ended_at IS NULL",
                (student_id,),
            ).fetchone()
            if active:
                raise ValueError("已有正在进行的学习会话")
            cursor = conn.execute(
                "INSERT INTO study_time_sessions (student_id, started_at) VALUES (?, ?)",
                (student_id, self._serialize(now)),
            )
            return {
                "session_id": cursor.lastrowid,
                "started_at": self._serialize(now),
                "active": True,
            }

    def pause(self, student_id: str) -> dict:
        now = self._now()
        with self._connection() as conn:
            self._ensure_account(conn, student_id, now)
            active = conn.execute(
                "SELECT * FROM study_time_sessions WHERE student_id=? AND ended_at IS NULL",
                (student_id,),
            ).fetchone()
            if not active:
                raise ValueError("当前没有正在进行的学习会话")
            started_at = datetime.fromisoformat(active["started_at"])
            duration = max(0, int((now - started_at).total_seconds()))
            conn.execute(
                "UPDATE study_time_sessions SET ended_at=?, duration_seconds=? WHERE session_id=?",
                (self._serialize(now), duration, active["session_id"]),
            )
        return self.get_summary(student_id)

    end = pause

    def get_summary(self, student_id: str) -> dict:
        now = self._now()
        current_week = self._week_start(now)
        with self._connection() as conn:
            self._ensure_account(conn, student_id, now)
            account = conn.execute(
                "SELECT * FROM study_time_accounts WHERE student_id=?",
                (student_id,),
            ).fetchone()
            sessions = conn.execute(
                "SELECT * FROM study_time_sessions WHERE student_id=?",
                (student_id,),
            ).fetchall()

        week_seconds = 0
        total_seconds = int(account["initial_seconds"])
        if account["initial_week_start"] == current_week.date().isoformat():
            week_seconds += int(account["initial_seconds"])

        for session in sessions:
            started_at = datetime.fromisoformat(session["started_at"])
            ended_at = datetime.fromisoformat(session["ended_at"]) if session["ended_at"] else now
            duration = max(0, int((ended_at - started_at).total_seconds()))
            total_seconds += duration
            overlap_start = max(started_at, current_week)
            if ended_at > overlap_start:
                week_seconds += int((ended_at - overlap_start).total_seconds())

        active = next((s for s in sessions if s["ended_at"] is None), None)
        return {
            "student_id": student_id,
            "week_seconds": week_seconds,
            "total_seconds": total_seconds,
            "active": bool(active),
            "session_id": active["session_id"] if active else None,
            "started_at": active["started_at"] if active else None,
        }
