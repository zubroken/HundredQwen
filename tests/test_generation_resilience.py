import tempfile
import unittest
from pathlib import Path

from models.resources import ResourceDB
from services.resource_generation_service import ResourceGenerationService
from tests.test_resource_generation_service import (
    RecordingAgent,
    StubDB,
    StubKnowledgeBase,
    StubLearningPathAgent,
)


class GenerationResilienceTest(unittest.TestCase):
    def make_service(self, path, clock, timeout_seconds=30):
        agents = {
            "document": RecordingAgent("DocumentAgent", "generate_document", "document"),
            "mindmap": RecordingAgent("MindMapAgent", "generate_mindmap", "mindmap"),
            "exercise": RecordingAgent("ExerciseAgent", "generate_exercises", "exercise"),
            "reading": RecordingAgent("ReadingAgent", "generate_readings", "reading"),
            "code_example": RecordingAgent("CodeExampleAgent", "generate_code_example", "code_example"),
        }
        return ResourceGenerationService(
            db=StubDB(),
            resource_db=ResourceDB(str(path)),
            knowledge_base=StubKnowledgeBase(),
            document_agent=agents["document"],
            mindmap_agent=agents["mindmap"],
            exercise_agent=agents["exercise"],
            reading_agent=agents["reading"],
            code_example_agent=agents["code_example"],
            learning_path_agent=StubLearningPathAgent(),
            agent_timeout_seconds=timeout_seconds,
            monotonic_clock=clock,
        )

    def test_slow_agent_returns_partial_bundle_with_fallback(self):
        timestamps = iter([0.0, 2.5])
        with tempfile.TemporaryDirectory() as tmpdir:
            service = self.make_service(
                Path(tmpdir) / "resources.json", lambda: next(timestamps), timeout_seconds=1
            )

            result = service.generate_bundle(
                {
                    "student_id": "stu_001",
                    "course_name": "AI",
                    "topic": "Transformer attention",
                    "resource_types": ["document"],
                }
            )

        self.assertEqual(result["status"], "partial")
        self.assertTrue(result["resources"][0]["fallback"])
        self.assertIn("timed out", " ".join(result["warnings"]))

    def test_response_contains_sanitized_agent_timing_log(self):
        timestamps = iter([10.0, 10.125])
        with tempfile.TemporaryDirectory() as tmpdir:
            service = self.make_service(Path(tmpdir) / "resources.json", lambda: next(timestamps))

            result = service.generate_bundle(
                {
                    "student_id": "stu_001",
                    "course_name": "AI",
                    "topic": "Transformer attention",
                    "resource_types": ["document"],
                }
            )

        entry = result["agent_logs"][0]
        self.assertEqual(entry["agent_name"], "DocumentAgent")
        self.assertEqual(entry["duration_ms"], 125)
        self.assertEqual(entry["status"], "completed")
        self.assertEqual(entry["warning_count"], 0)
        self.assertNotIn("topic", entry)
        self.assertNotIn("student_id", entry)


if __name__ == "__main__":
    unittest.main()
