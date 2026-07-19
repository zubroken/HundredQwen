import unittest

from agents.learning_path_agent import LearningPathAgent
from models.profile import StudentProfile
from models.resources import DocumentResource


class StubLLM:
    def __init__(self, reply):
        self.reply = reply
        self.calls = []

    def chat(self, system_prompt, message):
        self.calls.append((system_prompt, message))
        return self.reply


class StubModelGateway:
    def __init__(self, backend):
        self.backend = backend
        self.get_calls = []

    def get(self, name=None):
        self.get_calls.append(name)
        return self.backend


class LearningPathAgentTest(unittest.TestCase):
    def make_profile(self):
        return StudentProfile(
            student_id="stu_001",
            password="",
            name="test-user",
            school="",
            major="AI",
            grade="freshman",
            knowledge_base="basic",
            cognitive_style="logical",
            weak_points=["probability"],
            learning_goals=["learn ml"],
            learning_pace="medium",
            interest_topics=["NLP"],
            preferred_resource_types=["code"],
            programming_exp="Python basics",
            avatar="avatar-1",
        )

    def make_resources(self):
        return {
            "document": DocumentResource(
                resource_id="doc_001",
                title="doc",
                content={},
                tags=[],
                course_name="course",
                created_at="2024-01-01 00:00:00",
                student_id="stu_001",
            )
        }

    def test_generate_path_uses_llm_when_gateway_missing(self):
        llm = StubLLM(
            '{"title":"path set","description":"desc","nodes":[{"order":1,"title":"step1","description":"d1","estimated_hours":2,"prerequisites":[]}],"total_estimated_hours":2,"difficulty":"beginner"}'
        )
        agent = LearningPathAgent(llm_service=llm)

        path = agent.generate_path(self.make_profile(), self.make_resources())

        self.assertEqual(len(llm.calls), 1)
        self.assertEqual(path.title, "path set")
        self.assertEqual(path.nodes[0].title, "step1")
        self.assertEqual(path.nodes[0].resource_ids, ["doc_001"])

    def test_generate_path_prefers_gateway_default_backend(self):
        llm = StubLLM('{"title":"llm path"}')
        gateway_backend = StubLLM(
            '{"title":"gateway path","description":"desc","nodes":[{"order":1,"title":"step1","description":"d1","estimated_hours":2,"prerequisites":[]}],"total_estimated_hours":2,"difficulty":"beginner"}'
        )
        gateway = StubModelGateway(gateway_backend)
        agent = LearningPathAgent(llm_service=llm, model_gateway=gateway)

        path = agent.generate_path(self.make_profile(), self.make_resources())

        self.assertEqual(gateway.get_calls, [None])
        self.assertEqual(len(gateway_backend.calls), 1)
        self.assertEqual(llm.calls, [])
        self.assertEqual(path.title, "gateway path")


if __name__ == "__main__":
    unittest.main()
