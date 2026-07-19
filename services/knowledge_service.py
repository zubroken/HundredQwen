from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import HTTPException

from services.docx_exporter import DocxExporter
from services.knowledge_base import KnowledgeBase
from services.paper_fetcher import PaperFetcher

logger = logging.getLogger(__name__)


class KnowledgeService:
    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        paper_fetcher: PaperFetcher,
        docx_exporter: DocxExporter,
    ):
        self.knowledge_base = knowledge_base
        self.paper_fetcher = paper_fetcher
        self.docx_exporter = docx_exporter

    def list_documents(self) -> Dict[str, List[dict]]:
        return {"documents": self.knowledge_base.list_documents()}

    def search(
        self,
        query: str,
        type_filter: str = "all",
        doc_id: str = "",
        include_arxiv: bool = False,
    ) -> Dict[str, Any]:
        result = self.knowledge_base.search(query, type_filter=type_filter, doc_id=doc_id)

        arxiv_results = []
        if include_arxiv:
            try:
                arxiv_results = self.paper_fetcher.search(query, max_results=5)
            except Exception as exc:
                logger.warning(f"arXiv 搜索失败: {exc}")

        return {
            "query": query,
            "local": result,
            "arxiv": arxiv_results,
            "documents": self.knowledge_base.list_documents(),
        }

    def export_entry(
        self,
        entry_id: str = "",
        title: str = "",
        text: str = "",
        full_text: str = "",
        source: str = "",
        authors: list | None = None,
        published: str = "",
        keywords: list | None = None,
    ) -> Dict[str, Any]:
        entry = {
            "entry_id": entry_id,
            "title": title,
            "text": text,
            "full_text": full_text or text,
            "source": source or "知识库",
            "authors": authors or [],
            "published": published,
            "keywords": keywords or [],
        }

        try:
            filepath = self.docx_exporter.export_entry(entry)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"导出失败: {exc}") from exc

        return {"success": True, "filepath": filepath, "message": "导出成功"}

    def get_stats(self) -> Dict[str, Any]:
        return self.knowledge_base.get_stats()
