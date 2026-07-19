import unittest

from services.knowledge_service import KnowledgeService


class StubKnowledgeBase:
    def __init__(self):
        self.search_calls = []
        self.documents = [{"id": "doc-1", "title": "AI 导论"}]
        self.stats = {"documents": 1, "chunks": 3, "types": {"pdf": 1}}

    def list_documents(self):
        return self.documents

    def search(self, query, type_filter="all", doc_id=""):
        self.search_calls.append((query, type_filter, doc_id))
        return {
            "results": [
                {
                    "id": "chunk-1",
                    "title": "感知机",
                    "text": "用于分类的基础模型",
                    "type": "concept",
                }
            ]
        }

    def get_stats(self):
        return self.stats


class StubPaperFetcher:
    def __init__(self):
        self.calls = []

    def search(self, query, max_results=5):
        self.calls.append((query, max_results))
        return [{"id": "1234.5678", "title": "Transformer"}]


class StubDocxExporter:
    def __init__(self):
        self.exported_entry = None

    def export_entry(self, entry):
        self.exported_entry = entry
        return "C:/tmp/export.docx"


class KnowledgeServiceTest(unittest.TestCase):
    def setUp(self):
        self.kb = StubKnowledgeBase()
        self.paper_fetcher = StubPaperFetcher()
        self.docx_exporter = StubDocxExporter()
        self.service = KnowledgeService(
            knowledge_base=self.kb,
            paper_fetcher=self.paper_fetcher,
            docx_exporter=self.docx_exporter,
        )

    def test_list_documents_wraps_result(self):
        result = self.service.list_documents()

        self.assertEqual(result, {"documents": self.kb.documents})

    def test_search_without_arxiv_keeps_external_results_empty(self):
        result = self.service.search(
            query="机器学习",
            type_filter="concept",
            doc_id="doc-1",
            include_arxiv=False,
        )

        self.assertEqual(self.kb.search_calls, [("机器学习", "concept", "doc-1")])
        self.assertEqual(self.paper_fetcher.calls, [])
        self.assertEqual(result["query"], "机器学习")
        self.assertEqual(result["local"]["results"][0]["id"], "chunk-1")
        self.assertEqual(result["arxiv"], [])
        self.assertEqual(result["documents"], self.kb.documents)

    def test_search_with_arxiv_appends_external_results(self):
        result = self.service.search(
            query="Transformer",
            include_arxiv=True,
        )

        self.assertEqual(self.paper_fetcher.calls, [("Transformer", 5)])
        self.assertEqual(result["arxiv"], [{"id": "1234.5678", "title": "Transformer"}])

    def test_export_entry_applies_default_fields(self):
        result = self.service.export_entry(
            entry_id="entry-1",
            title="知识点",
            text="摘要",
            full_text="",
            source="",
            authors=["Alice"],
            published="2024-01-01",
            keywords=["NLP"],
        )

        self.assertEqual(result["success"], True)
        self.assertEqual(result["filepath"], "C:/tmp/export.docx")
        self.assertEqual(
            self.docx_exporter.exported_entry,
            {
                "title": "知识点",
                "text": "摘要",
                "full_text": "摘要",
                "source": "知识库",
                "entry_id": "entry-1",
                "authors": ["Alice"],
                "published": "2024-01-01",
                "keywords": ["NLP"],
            },
        )

    def test_get_stats_returns_knowledge_base_stats(self):
        self.assertEqual(self.service.get_stats(), self.kb.stats)


if __name__ == "__main__":
    unittest.main()
