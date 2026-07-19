from __future__ import annotations

from fastapi import FastAPI

from api.schemas import KnowledgeExportRequest, KnowledgeSearchRequest
from services.app_services import AppServices


def register_knowledge_routes(app: FastAPI, services: AppServices) -> None:
    @app.get("/api/knowledge/documents")
    async def list_documents():
        return services.knowledge_service.list_documents()

    @app.post("/api/knowledge/search")
    async def search_knowledge(req: KnowledgeSearchRequest):
        return services.knowledge_service.search(
            query=req.query,
            type_filter=req.type_filter,
            doc_id=req.doc_id,
            include_arxiv=req.include_arxiv,
        )

    @app.post("/api/knowledge/export")
    async def export_knowledge(req: KnowledgeExportRequest):
        return services.knowledge_service.export_entry(
            entry_id=req.entry_id,
            title=req.title,
            text=req.text,
            full_text=req.full_text,
            source=req.source,
            authors=req.authors,
            published=req.published,
            keywords=req.keywords,
        )

    @app.get("/api/knowledge/stats")
    async def get_knowledge_stats():
        return services.knowledge_service.get_stats()
