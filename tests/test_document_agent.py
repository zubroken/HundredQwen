import unittest

from agents.document_agent import DocumentAgent
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


class DocumentAgentTest(unittest.TestCase):
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

    def test_generate_document_uses_llm_when_gateway_missing(self):
        llm = StubLLM(
            '{"title":"doc set","sections":[{"title":"s1","content":"body","level":1}],"key_concepts":["k1"]}'
        )
        agent = DocumentAgent(llm_service=llm)

        resource = agent.generate_document(self.make_profile(), "generate document")

        self.assertEqual(len(llm.calls), 1)
        self.assertEqual(resource.title, "doc set")
        self.assertEqual(resource.content["sections"][0]["title"], "s1")

    def test_generate_document_prefers_gateway_default_backend(self):
        llm = StubLLM('{"title":"llm doc"}')
        gateway_backend = StubLLM(
            '{"title":"gateway doc","sections":[{"title":"s1","content":"body","level":1}],"key_concepts":["k1"]}'
        )
        gateway = StubModelGateway(gateway_backend)
        agent = DocumentAgent(llm_service=llm, model_gateway=gateway)

        resource = agent.generate_document(self.make_profile(), "generate document")

        self.assertEqual(gateway.get_calls, [None])
        self.assertEqual(len(gateway_backend.calls), 1)
        self.assertEqual(llm.calls, [])
        self.assertEqual(resource.title, "gateway doc")


if __name__ == "__main__":
    unittest.main()
