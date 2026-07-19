import tempfile
import unittest
from pathlib import Path

from models.profile import StudentProfile
from models.resources import ResourceDB, ResourceType
from services.resource_generation_service import ResourceGenerationService


class StubDB:
    def __init__(self):
        self.profile = StudentProfile(
            student_id="stu_001",
            major="AI",
            weak_points=["attention"],
            learning_goals=["learn Transformer"],
            interest_topics=["NLP"],
            preferred_resource_types=["document"],
            programming_exp="Python",
        )

    def get_student(self, student_id):
        return self.profile if student_id == self.profile.student_id else None


class StubKnowledgeBase:
    def retrieve(self, query, top_k=5, doc_id=""):
        return [
            {
                "id": "chunk-1",
                "doc_id": "doc-1",
                "doc_title": "AI Textbook",
                "page": "8",
                "text": "Transformer attention compares queries and keys.",
                "score": 4,
            }
        ]


class RecordingAgent:
    def __init__(self, name, method_name, resource_type):
        self.name = name
        self.method_name = method_name
        self.resource_type = resource_type
        self.calls = []
        setattr(self, method_name, self._generate)

    def _generate(self, profile, request):
        from models.resources import Resource

        self.calls.append((profile.student_id, request))
        return Resource(
            resource_id=f"{self.resource_type}-1",
            title=f"{self.name} output",
            resource_type=self.resource_type,
            content={"summary": f"{self.name} summary"},
            student_id=profile.student_id,
        )


class FailingAgent:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        if name.startswith("generate_"):
            def fail(profile, request):
                raise RuntimeError("model unavailable")
            return fail
        raise AttributeError(name)


class StubLearningPathAgent:
    name = "LearningPathAgent"

    def generate_path(self, profile, resources):
        from models.resources import LearningPath, PathNode

        resource_ids = [resource.resource_id for resource in resources.values()]
        return LearningPath(
            path_id="path-1",
            student_id=profile.student_id,
            course_name="AI",
            title="Transformer path",
            nodes=[
                PathNode(
                    node_id="node-1",
                    title="Read and practice",
                    resource_ids=resource_ids,
                    order=1,
                )
            ],
            total_estimated_hours=2,
        )


class ResourceGenerationServiceTest(unittest.TestCase):
    def make_service(self, path):
        agents = {
            "document": RecordingAgent("DocumentAgent", "generate_document", ResourceType.DOCUMENT),
            "mindmap": RecordingAgent("MindMapAgent", "generate_mindmap", ResourceType.MINDMAP),
            "exercise": RecordingAgent("ExerciseAgent", "generate_exercises", ResourceType.EXERCISE),
            "reading": RecordingAgent("ReadingAgent", "generate_readings", ResourceType.READING),
            "code_example": RecordingAgent("CodeExampleAgent", "generate_code_example", ResourceType.CODE_EXAMPLE),
        }
        service = ResourceGenerationService(
            db=StubDB(),
            resource_db=ResourceDB(str(path)),
            knowledge_base=StubKnowledgeBase(),
            document_agent=agents["document"],
            mindmap_agent=agents["mindmap"],
            exercise_agent=agents["exercise"],
            reading_agent=agents["reading"],
            code_example_agent=agents["code_example"],
            learning_path_agent=StubLearningPathAgent(),
        )
        return service, agents

    def test_generate_bundle_calls_five_agents_and_persists_bundle(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            service, agents = self.make_service(Path(tmpdir) / "resources.json")

            result = service.generate_bundle(
                {
                    "student_id": "stu_001",
                    "course_name": "AI",
                    "topic": "Transformer attention",
                    "difficulty": "intermediate",
                    "resource_types": [
                        "document",
                        "mindmap",
                        "exercise",
                        "reading",
                        "code_example",
                    ],
                }
            )

            self.assertEqual(result["status"], "completed")
            self.assertEqual(len(result["resources"]), 5)
            self.assertEqual(result["path"]["path_id"], "path-1")
            self.assertEqual(result["citations"][0]["source_id"], "doc-1")
            self.assertEqual(
                [agent.calls[0][0] for agent in agents.values()],
                ["stu_001", "stu_001", "stu_001", "stu_001", "stu_001"],
            )
            self.assertEqual(service.list_bundles("stu_001")[0]["bundle_id"], result["bundle_id"])

    def test_update_path_node_persists_status(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            service, _ = self.make_service(Path(tmpdir) / "resources.json")
            result = service.generate_bundle(
                {
                    "student_id": "stu_001",
                    "course_name": "AI",
                    "topic": "Transformer attention",
                    "difficulty": "intermediate",
                    "resource_types": ["document", "mindmap", "exercise", "reading", "code_example"],
                }
            )

            updated = service.update_path_node(result["path"]["path_id"], "node-1", "completed")

            self.assertEqual(updated["nodes"][0]["status"], "completed")
            self.assertEqual(service.get_learning_path("stu_001")["nodes"][0]["status"], "completed")

    def test_model_failure_uses_deterministic_fallback_resources(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            service, _ = self.make_service(Path(tmpdir) / "resources.json")
            service.agents["document"] = (FailingAgent("DocumentAgent"), "generate_document")

            result = service.generate_bundle(
                {
                    "student_id": "stu_001",
                    "course_name": "AI",
                    "topic": "Transformer attention",
                    "difficulty": "intermediate",
                    "resource_types": ["document", "mindmap", "exercise", "reading", "code_example"],
                }
            )

            document = [r for r in result["resources"] if r["resource_type"] == "document"][0]
            self.assertEqual(result["status"], "partial")
            self.assertTrue(document["fallback"])
            self.assertIn("model unavailable", " ".join(result["warnings"]))


if __name__ == "__main__":
    unittest.main()
