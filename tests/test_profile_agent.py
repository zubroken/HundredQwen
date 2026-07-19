import unittest

from agents.profile_agent import ProfileAgent


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


class ProfileAgentTest(unittest.TestCase):
    def test_build_profile_from_dialogue_uses_llm_when_gateway_missing(self):
        llm = StubLLM(
            '{"knowledge_base":"basic","cognitive_style":"logical","weak_points":["math"],'
            '"learning_goals":["ml"],"learning_pace":"medium","interest_topics":["nlp"],'
            '"preferred_resource_types":["code"],"programming_exp":"python"}'
        )
        agent = ProfileAgent(llm_service=llm)

        profile = agent.build_profile_from_dialogue(
            [{"role": "user", "content": "I like machine learning"}]
        )

        self.assertEqual(len(llm.calls), 1)
        self.assertEqual(profile.knowledge_base, "basic")
        self.assertEqual(profile.learning_goals, ["ml"])

    def test_build_profile_from_dialogue_prefers_gateway_default_backend(self):
        llm = StubLLM('{"knowledge_base":"llm"}')
        gateway_backend = StubLLM(
            '{"knowledge_base":"gateway","cognitive_style":"visual","weak_points":[],"learning_goals":[],'
            '"learning_pace":"medium","interest_topics":[],"preferred_resource_types":[],"programming_exp":"none"}'
        )
        gateway = StubModelGateway(gateway_backend)
        agent = ProfileAgent(llm_service=llm, model_gateway=gateway)

        profile = agent.build_profile_from_dialogue(
            [{"role": "user", "content": "I prefer diagrams"}]
        )

        self.assertEqual(gateway.get_calls, [None])
        self.assertEqual(len(gateway_backend.calls), 1)
        self.assertEqual(llm.calls, [])
        self.assertEqual(profile.knowledge_base, "gateway")


if __name__ == "__main__":
    unittest.main()
