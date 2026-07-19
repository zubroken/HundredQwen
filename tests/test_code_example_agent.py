import unittest

from agents.code_example_agent import CodeExampleAgent
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


class CodeExampleAgentTest(unittest.TestCase):
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

    def test_generate_code_example_uses_llm_when_gateway_missing(self):
        llm = StubLLM(
            '{"title":"code set","language":"Python","code":"print(1)","setup_steps":["s1"],"hints":["h1"]}'
        )
        agent = CodeExampleAgent(llm_service=llm)

        resource = agent.generate_code_example(self.make_profile(), "generate code example")

        self.assertEqual(len(llm.calls), 1)
        self.assertEqual(resource.title, "code set")
        self.assertEqual(resource.content["language"], "Python")

    def test_generate_code_example_prefers_gateway_default_backend(self):
        llm = StubLLM('{"title":"llm code"}')
        gateway_backend = StubLLM(
            '{"title":"gateway code","language":"Python","code":"print(1)","setup_steps":["s1"],"hints":["h1"]}'
        )
        gateway = StubModelGateway(gateway_backend)
        agent = CodeExampleAgent(llm_service=llm, model_gateway=gateway)

        resource = agent.generate_code_example(self.make_profile(), "generate code example")

        self.assertEqual(gateway.get_calls, [None])
        self.assertEqual(len(gateway_backend.calls), 1)
        self.assertEqual(llm.calls, [])
        self.assertEqual(resource.title, "gateway code")


if __name__ == "__main__":
    unittest.main()
