from __future__ import annotations

from pathlib import Path


VERSION = "1.0.4"

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
CHAT_HISTORY_DIR = DATA_DIR / "chat_history"

DB_PATH = DATA_DIR / "app.db"
RESOURCES_PATH = DATA_DIR / "resources.json"
PAPERS_CACHE_PATH = KNOWLEDGE_DIR / "papers_cache.json"
