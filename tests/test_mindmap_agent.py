import unittest

from agents.mindmap_agent import MindMapAgent
from models.profile import StudentProfile


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


class MindMapAgentTest(unittest.TestCase):
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

    def test_generate_mindmap_uses_llm_when_gateway_missing(self):
        llm = StubLLM(
            '{"central_topic":"topic map","nodes":[{"id":"1","label":"root","parent_id":null,"description":"d","level":0}],"connections":[]}'
        )
        agent = MindMapAgent(llm_service=llm)

        resource = agent.generate_mindmap(self.make_profile(), "generate mindmap")

        self.assertEqual(len(llm.calls), 1)
        self.assertEqual(resource.title, "topic map")
        self.assertEqual(resource.content["nodes"][0]["label"], "root")

    def test_generate_mindmap_prefers_gateway_default_backend(self):
        llm = StubLLM('{"central_topic":"llm map"}')
        gateway_backend = StubLLM(
            '{"central_topic":"gateway map","nodes":[{"id":"1","label":"root","parent_id":null,"description":"d","level":0}],"connections":[]}'
        )
        gateway = StubModelGateway(gateway_backend)
        agent = MindMapAgent(llm_service=llm, model_gateway=gateway)

        resource = agent.generate_mindmap(self.make_profile(), "generate mindmap")

        self.assertEqual(gateway.get_calls, [None])
        self.assertEqual(len(gateway_backend.calls), 1)
        self.assertEqual(llm.calls, [])
        self.assertEqual(resource.title, "gateway map")


if __name__ == "__main__":
    unittest.main()
