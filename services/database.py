"""
SQLite 数据库服务 —— 存储学生账户和画像数据
"""
from __future__ import annotations
import hashlib
import sqlite3
import json
import os
from typing import Optional, List
from datetime import datetime
from models.profile import StudentProfile
from settings import DB_PATH


def _hash_password(password: str) -> str:
    """SHA-256 哈希密码，返回 hex 摘要"""
    return hashlib.sha256(password.encode()).hexdigest()


def _verify_password(password: str, stored: str) -> bool:
    """验证密码。兼容旧明文密码（非64位hex视为明文直接比较）"""
    if len(stored) == 64 and all(c in "0123456789abcdef" for c in stored):
        return _hash_password(password) == stored
    # 明文兼容：旧密码直接比较
    return password == stored


def get_connection() -> sqlite3.Connection:
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """创建表并插入默认账户（首次运行）"""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            name TEXT DEFAULT '',
            school TEXT DEFAULT '',
            major TEXT DEFAULT '',
            grade TEXT DEFAULT '',
            knowledge_base TEXT DEFAULT '',
            cognitive_style TEXT DEFAULT '',
            weak_points TEXT DEFAULT '[]',
            learning_goals TEXT DEFAULT '[]',
            learning_pace TEXT DEFAULT '',
            interest_topics TEXT DEFAULT '[]',
            preferred_resource_types TEXT DEFAULT '[]',
            programming_exp TEXT DEFAULT '',
            avatar TEXT DEFAULT 'avatar-1',
            created_at TEXT DEFAULT '',
            updated_at TEXT DEFAULT ''
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skill_tree_progress (
            student_id TEXT,
            chapter_id INTEGER,
            node_id TEXT,
            l1_status TEXT DEFAULT 'locked',
            l2_status TEXT DEFAULT 'locked',
            l3_status TEXT DEFAULT 'locked',
            l1_score INTEGER DEFAULT 0,
            l2_score INTEGER DEFAULT 0,
            l3_score INTEGER DEFAULT 0,
            updated_at TEXT DEFAULT '',
            PRIMARY KEY (student_id, chapter_id, node_id)
        )
    """)
    # 检查是否已有数据
    row = conn.execute("SELECT COUNT(*) FROM students").fetchone()
    if row[0] == 0:
        _seed_defaults(conn)
    conn.close()


def _seed_defaults(conn: sqlite3.Connection):
    """插入预设账户（仅人工智能专业）"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    defaults = [
        {
            "student_id": "stu_001",
            "password": _hash_password("1"),
            "name": "张三",
            "school": "华南理工大学",
            "major": "人工智能",
            "grade": "大三",
            "knowledge_base": "已学习Python、高等数学、线性代数、概率论、数据结构与算法，具备扎实的数学和编程基础，正在学习机器学习入门课程",
            "cognitive_style": "逻辑型（偏好通过系统性推理和结构化学习来掌握知识，擅长抽象概念理解）",
            "weak_points": json.dumps(["深度学习中的反向传播推导", "强化学习的数学原理", "Transformer注意力机制"], ensure_ascii=False),
            "learning_goals": json.dumps(["系统掌握机器学习与深度学习核心算法", "熟练使用PyTorch框架", "完成一个完整的AI项目（从数据处理到模型部署）"], ensure_ascii=False),
            "learning_pace": "中（大三学生，数学和编程基础扎实，但AI领域知识点密集，需要稳步推进）",
            "interest_topics": json.dumps(["机器学习", "深度学习", "自然语言处理", "计算机视觉", "强化学习"], ensure_ascii=False),
            "preferred_resource_types": json.dumps(["代码案例", "项目实战", "论文导读", "概念图解"], ensure_ascii=False),
            "programming_exp": "2年Python经验，熟悉NumPy/Pandas，了解PyTorch基础，有Git使用经验",
            "created_at": now,
            "updated_at": now,
        },
    ]
    for d in defaults:
        conn.execute("""
            INSERT INTO students (student_id, password, name, school, major, grade,
                knowledge_base, cognitive_style, weak_points, learning_goals,
                learning_pace, interest_topics, preferred_resource_types,
                programming_exp, avatar, created_at, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            d["student_id"], d["password"], d["name"], d["school"],
            d["major"], d["grade"], d["knowledge_base"], d["cognitive_style"],
            d["weak_points"], d["learning_goals"], d["learning_pace"],
            d["interest_topics"], d["preferred_resource_types"],
            d["programming_exp"], d.get("avatar", "avatar-1"), d["created_at"], d["updated_at"],
        ))
    conn.commit()


class DatabaseManager:
    """学生数据库管理器"""

    def get_student(self, student_id: str) -> Optional[StudentProfile]:
        conn = get_connection()
        row = conn.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
        conn.close()
        if not row:
            return None
        return self._row_to_profile(row)

    def verify_login(self, student_id: str, password: str) -> Optional[StudentProfile]:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id,)
        ).fetchone()
        conn.close()
        if not row:
            return None
        stored = row["password"]
        if not _verify_password(password, stored):
            return None
        # 迁移：如果是旧明文密码，自动升级为哈希
        if not (len(stored) == 64 and all(c in "0123456789abcdef" for c in stored)):
            self._upgrade_password(student_id, password)
        return self._row_to_profile(row)

    def save_profile(self, profile: StudentProfile):
        """保存或更新学生画像"""
        conn = get_connection()
        existing = conn.execute("SELECT student_id FROM students WHERE student_id=?", (profile.student_id,)).fetchone()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if existing:
            updates = profile.to_dict()
            updates.pop("student_id", None)
            updates.pop("created_at", None)
            updates.pop("conversation_history", None)
            self._update_internal(conn, profile.student_id, updates, now)
        else:
            hashed_pw = _hash_password(profile.password) if profile.password else _hash_password("1")
            conn.execute("""
                INSERT INTO students (student_id, password, name, school, major, grade,
                    knowledge_base, cognitive_style, weak_points, learning_goals,
                    learning_pace, interest_topics, preferred_resource_types,
                    programming_exp, avatar, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                profile.student_id, hashed_pw,
                profile.name, profile.school, profile.major, profile.grade,
                profile.knowledge_base, profile.cognitive_style,
                json.dumps(profile.weak_points, ensure_ascii=False),
                json.dumps(profile.learning_goals, ensure_ascii=False),
                profile.learning_pace,
                json.dumps(profile.interest_topics, ensure_ascii=False),
                json.dumps(profile.preferred_resource_types, ensure_ascii=False),
                profile.programming_exp, profile.avatar or "avatar-1", now, now,
            ))
        conn.commit()
        conn.close()

    def _upgrade_password(self, student_id: str, plaintext_password: str) -> None:
        """将旧明文密码升级为 SHA-256 哈希"""
        conn = get_connection()
        hashed = _hash_password(plaintext_password)
        conn.execute("UPDATE students SET password=? WHERE student_id=?", (hashed, student_id))
        conn.commit()
        conn.close()

    def update_profile(self, student_id: str, updates: dict) -> bool:
        conn = get_connection()
        result = self._update_internal(conn, student_id, updates)
        conn.commit()
        conn.close()
        return result

    def _update_internal(self, conn, student_id: str, updates: dict, timestamp: Optional[str] = None) -> bool:
        allowed = {
            "name", "school", "major", "grade", "knowledge_base",
            "cognitive_style", "weak_points", "learning_goals", "learning_pace",
            "interest_topics", "preferred_resource_types", "programming_exp", "avatar",
        }
        fields = []
        values = []
        for k, v in updates.items():
            if k in allowed:
                if isinstance(v, list):
                    v = json.dumps(v, ensure_ascii=False)
                fields.append(f"{k}=?")
                values.append(v)
        if not fields:
            return False
        values.append(timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        values.append(student_id)
        conn.execute(f"UPDATE students SET {', '.join(fields)}, updated_at=? WHERE student_id=?", values)
        return True

    def delete_student(self, student_id: str) -> bool:
        conn = get_connection()
        conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        deleted = conn.total_changes > 0
        conn.commit()
        conn.close()
        return deleted

    def list_all(self) -> List[StudentProfile]:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM students").fetchall()
        conn.close()
        return [self._row_to_profile(r) for r in rows]

    def get_skill_tree_progress(self, student_id: str) -> dict:
        """返回 { 'chapter_id-node_id': {l1_status, l2_status, l3_status, scores} }"""
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM skill_tree_progress WHERE student_id=?",
            (student_id,)
        ).fetchall()
        conn.close()
        result = {}
        for r in rows:
            key = f"{r['chapter_id']}-{r['node_id']}"
            result[key] = {
                "l1_status": r["l1_status"], "l2_status": r["l2_status"],
                "l3_status": r["l3_status"], "l1_score": r["l1_score"],
                "l2_score": r["l2_score"], "l3_score": r["l3_score"],
            }
        return result

    def save_skill_tree_progress(self, student_id: str, chapter_id: int, node_id: str,
                                  level: str, status: str, score: int = 0) -> None:
        """更新或插入某节点某层进度"""
        conn = get_connection()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("""
            INSERT INTO skill_tree_progress (student_id, chapter_id, node_id,
                l1_status, l2_status, l3_status, l1_score, l2_score, l3_score, updated_at)
            VALUES (?,?,?,'locked','locked','locked',0,0,0,?)
            ON CONFLICT(student_id, chapter_id, node_id) DO NOTHING
        """, (student_id, chapter_id, node_id, now))
        status_col = f"{level}_status"
        score_col = f"{level}_score"
        conn.execute(
            f"UPDATE skill_tree_progress SET {status_col}=?, {score_col}=?, updated_at=? "
            "WHERE student_id=? AND chapter_id=? AND node_id=?",
            (status, score, now, student_id, chapter_id, node_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def _row_to_profile(row: sqlite3.Row) -> StudentProfile:
        return StudentProfile(
            student_id=row["student_id"],
            password=row["password"],
            name=row["name"] or "",
            school=row["school"] or "",
            major=row["major"] or "",
            grade=row["grade"] or "",
            knowledge_base=row["knowledge_base"] or "",
            cognitive_style=row["cognitive_style"] or "",
            weak_points=json.loads(row["weak_points"] or "[]"),
            learning_goals=json.loads(row["learning_goals"] or "[]"),
            learning_pace=row["learning_pace"] or "",
            interest_topics=json.loads(row["interest_topics"] or "[]"),
            preferred_resource_types=json.loads(row["preferred_resource_types"] or "[]"),
            programming_exp=row["programming_exp"] or "",
            avatar=row["avatar"] or "avatar-1",
            created_at=row["created_at"] or "",
            updated_at=row["updated_at"] or "",
        )
