import unittest

from services.citation_service import CitationService


class CitationServiceTest(unittest.TestCase):
    def test_builds_citations_from_real_chunks(self):
        service = CitationService()

        result = service.from_chunks(
            [
                {
                    "id": "chunk-1",
                    "doc_id": "doc-1",
                    "doc_title": "AI Textbook",
                    "page": "12",
                    "text": "Attention assigns different weights to tokens.",
                    "score": 3,
                }
            ]
        )

        self.assertEqual(result["evidence_level"], "supported")
        self.assertEqual(result["citations"][0]["source_id"], "doc-1")
        self.assertEqual(result["citations"][0]["title"], "AI Textbook")
        self.assertEqual(result["citations"][0]["page"], "12")
        self.assertIn("Attention", result["citations"][0]["snippet"])
        self.assertEqual(result["citations"][0]["score"], 3)

    def test_empty_chunks_mark_evidence_insufficient(self):
        service = CitationService()

        result = service.from_chunks([])

        self.assertEqual(result["evidence_level"], "insufficient")
        self.assertEqual(result["citations"], [])
        self.assertTrue(result["warnings"])


if __name__ == "__main__":
    unittest.main()
