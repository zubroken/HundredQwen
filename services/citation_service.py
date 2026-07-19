from __future__ import annotations


class CitationService:
    def from_chunks(self, chunks: list[dict]) -> dict:
        if not chunks:
            return {
                "evidence_level": "insufficient",
                "citations": [],
                "warnings": ["Knowledge base did not return enough evidence; please verify."],
            }

        citations = []
        for chunk in chunks:
            text = chunk.get("text") or chunk.get("full_text") or ""
            citations.append(
                {
                    "source_id": chunk.get("doc_id") or chunk.get("id", ""),
                    "title": chunk.get("doc_title") or chunk.get("title", ""),
                    "page": chunk.get("page", ""),
                    "snippet": text[:240],
                    "score": chunk.get("score", 0),
                }
            )
        return {
            "evidence_level": "supported",
            "citations": citations,
            "warnings": [],
        }
