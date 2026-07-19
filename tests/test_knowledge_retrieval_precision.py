import unittest

from services.knowledge_base import KnowledgeBase


class KnowledgeRetrievalPrecisionTest(unittest.TestCase):
    def make_knowledge_base(self):
        kb = KnowledgeBase()
        kb.chunks = [
            {
                "id": "textbook-transformer",
                "doc_id": "ai-textbook",
                "doc_title": "人工智能导论：Transformer 注意力机制",
                "text": "Transformer 注意力机制通过查询、键和值计算上下文表示。",
                "page": "42",
                "type": "textbook",
                "difficulty": "intermediate",
            },
            {
                "id": "duplicate-transformer",
                "doc_id": "ai-textbook",
                "doc_title": "人工智能导论：Transformer 注意力机制",
                "text": "注意力机制用于动态计算查询、键和值之间的关联。",
                "page": "42",
                "type": "textbook",
                "difficulty": "intermediate",
            },
            {
                "id": "generic-mechanism",
                "doc_id": "generic-notes",
                "doc_title": "机器学习基础",
                "text": "机制用于解释模型的工作过程。",
                "page": "3",
                "type": "concept",
                "difficulty": "easy",
            },
        ]
        for index, chunk in enumerate(kb.chunks):
            kb._add_to_index(index, chunk["text"] + " " + chunk["doc_title"])
        kb._loaded = True
        return kb

    def test_phrase_and_title_match_outrank_generic_keyword_match(self):
        results = self.make_knowledge_base().retrieve("Transformer 注意力机制", top_k=5)

        self.assertIn("查询", results[0]["text"])
        self.assertGreater(results[0]["score_details"]["phrase"], 0)
        self.assertIn("标题匹配", results[0]["match_reasons"])
        self.assertEqual(results[0]["evidence_level"], "supported")

    def test_alias_expansion_finds_query_key_value_content(self):
        results = self.make_knowledge_base().retrieve("QKV", top_k=5)

        self.assertIn("查询", results[0]["text"])
        self.assertGreater(results[0]["score_details"]["alias"], 0)

    def test_same_document_page_is_deduplicated(self):
        results = self.make_knowledge_base().retrieve("注意力机制", top_k=5)

        same_page = [item for item in results if item["doc_id"] == "ai-textbook" and item["page"] == "42"]
        self.assertEqual(len(same_page), 1)

    def test_unknown_query_returns_insufficient_evidence(self):
        result = self.make_knowledge_base().search("量子纠缠医学诊断")

        self.assertEqual(result["results"], [])
        self.assertEqual(result["evidence_level"], "insufficient")
        self.assertIn("知识库未找到充分依据", result["warnings"][0])


if __name__ == "__main__":
    unittest.main()
