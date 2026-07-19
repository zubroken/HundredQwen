"""
arXiv 论文搜索与下载服务
"""
from __future__ import annotations
import json
import os
import logging
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Optional
from settings import KNOWLEDGE_DIR, PAPERS_CACHE_PATH

logger = logging.getLogger(__name__)

ARXIV_API = "http://export.arxiv.org/api/query"
CACHE_FILE = PAPERS_CACHE_PATH


class PaperFetcher:
    """arXiv 论文搜索"""

    def __init__(self):
        self._cache: dict = {}
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._cache = {}

    def _save_cache(self):
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self._cache, f, ensure_ascii=False, indent=2)

    def search(self, query: str, max_results: int = 10) -> List[dict]:
        """搜索 arXiv"""
        cache_key = f"{query}_{max_results}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        params = urllib.parse.urlencode({
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        })
        url = f"{ARXIV_API}?{params}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HundredQwen/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read().decode("utf-8")
            results = self._parse_response(data)
            self._cache[cache_key] = results
            self._save_cache()
            return results
        except Exception as e:
            logger.warning(f"arXiv 搜索失败: {e}")
            return self._cache.get(cache_key, [])

    def _parse_response(self, xml_data: str) -> List[dict]:
        root = ET.fromstring(xml_data)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        papers = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            arxiv_id = entry.find("atom:id", ns)
            published = entry.find("atom:published", ns)

            authors = []
            for author in entry.findall("atom:author", ns):
                name = author.find("atom:name", ns)
                if name is not None:
                    authors.append(name.text)

            link = ""
            for l in entry.findall("atom:link", ns):
                if l.get("title") == "pdf":
                    link = l.get("href", "")
                    break

            arxiv_id_str = arxiv_id.text.split("/abs/")[-1] if arxiv_id is not None else ""
            papers.append({
                "id": arxiv_id_str,
                "title": (title.text or "").strip().replace("\n", " "),
                "authors": authors[:5],
                "summary": (summary.text or "").strip()[:500].replace("\n", " "),
                "published": (published.text or "")[:10] if published is not None else "",
                "pdf_url": link,
                "arxiv_url": arxiv_id.text if arxiv_id is not None else "",
                "source": "arxiv",
            })
        return papers

    def fetch_pdf(self, arxiv_id: str) -> Optional[str]:
        """下载 arXiv PDF 到 papers/ 目录"""
        pdf_dir = KNOWLEDGE_DIR / "papers"
        os.makedirs(pdf_dir, exist_ok=True)
        filepath = pdf_dir / f"{arxiv_id}.pdf"

        if os.path.exists(filepath):
            return str(filepath)

        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        try:
            req = urllib.request.Request(pdf_url, headers={"User-Agent": "HundredQwen/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                with open(filepath, "wb") as f:
                    f.write(resp.read())
            logger.info(f"下载 arXiv PDF: {arxiv_id}")
            return str(filepath)
        except Exception as e:
            logger.error(f"下载 PDF 失败 {arxiv_id}: {e}")
            return None
