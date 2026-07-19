import unittest

from fastapi import HTTPException

from models.profile import StudentProfile
from services.chat_service import ChatService


class StubDatabase:
    def __init__(self, profile=None):
        self.profile = profile
        self.saved_profiles = []

    def get_student(self, student_id):
        return self.profile

    def save_profile(self, profile):
        self.saved_profiles.append(profile)


class StubLLMService:
    def __init__(self, reply="reply"):
        self.reply = reply
        self.calls = []

    def chat(self, system_prompt, message, **kwargs):
        self.calls.append((system_prompt, message, kwargs.get("temperature")))
        return self.reply


class StubModelGateway:
    def __init__(self, backend):
        self.backend = backend
        self.get_calls = []

    def get(self, name=None):
        self.get_calls.append(name)
        return self.backend


class StubProfileAgent:
    def __init__(self, updated_profile=None, error=None):
        self.updated_profile = updated_profile
        self.error = error
        self.calls = []

    def update_profile(self, profile, dialogue):
        self.calls.append((profile, dialogue))
        if self.error:
            raise self.error
        return self.updated_profile


class StubChatHistoryService:
    def __init__(self, context="history"):
        self.context = context
        self.context_calls = []
        self.append_calls = []

    def build_context(self, student_id):
        self.context_calls.append(student_id)
        return self.context

    def append_turn(self, student_id, message, reply):
        self.append_calls.append((student_id, message, reply))


class StubChatPromptService:
    def __init__(self, kb_context="kb", system_prompt="system"):
        self.kb_context = kb_context
        self.system_prompt = system_prompt
        self.kb_calls = []
        self.prompt_calls = []

    def build_kb_context(self, message):
        self.kb_calls.append(message)
        return self.kb_context

    def build_system_prompt(self, profile, hist_context, kb_context):
        self.prompt_calls.append((profile, hist_context, kb_context))
        return self.system_prompt


class ChatServiceTest(unittest.TestCase):
    def make_profile(self, student_id="stu_001", name="test-user"):
        return StudentProfile(
            student_id=student_id,
            password="",
            name=name,
            school="",
            major="AI",
            grade="freshman",
            knowledge_base="basic",
            cognitive_style="logical",
            weak_points=[],
            learning_goals=["learn ml"],
            learning_pace="medium",
            interest_topics=["NLP"],
            preferred_resource_types=["code"],
            programming_exp="Python basics",
            avatar="avatar-1",
        )

    def test_chat_returns_reply_and_updated_public_profile(self):
        profile = self.make_profile()
        updated_profile = self.make_profile(name="updated-user")
        db = StubDatabase(profile=profile)
        llm_service = StubLLMService(reply="answer")
        profile_agent = StubProfileAgent(updated_profile=updated_profile)
        history_service = StubChatHistoryService()
        prompt_service = StubChatPromptService()
        service = ChatService(db, llm_service, profile_agent, history_service, prompt_service)

        result = service.chat("stu_001", "what is supervised learning")

        self.assertEqual(prompt_service.kb_calls, ["what is supervised learning"])
        self.assertEqual(history_service.context_calls, ["stu_001"])
        self.assertEqual(prompt_service.prompt_calls, [(profile, "history", "kb")])
        self.assertEqual(llm_service.calls[0][:2], ("system", "what is supervised learning"))
        self.assertEqual(
            history_service.append_calls,
            [("stu_001", "what is supervised learning", "answer")],
        )
        self.assertEqual(len(db.saved_profiles), 1)
        self.assertEqual(
            profile_agent.calls,
            [(profile, [{"role": "user", "content": "what is supervised learning"}])],
        )
        self.assertEqual(result["reply"], "answer")
        self.assertEqual(result["profile"]["name"], "updated-user")
        self.assertNotIn("password", result["profile"])

    def test_chat_prefers_model_gateway_default_backend_when_present(self):
        profile = self.make_profile()
        db = StubDatabase(profile=profile)
        llm_service = StubLLMService(reply="llm-answer")
        gateway_backend = StubLLMService(reply="gateway-answer")
        model_gateway = StubModelGateway(gateway_backend)
        profile_agent = StubProfileAgent(updated_profile=profile)
        history_service = StubChatHistoryService()
        prompt_service = StubChatPromptService()
        service = ChatService(
            db,
            llm_service,
            profile_agent,
            history_service,
            prompt_service,
            model_gateway=model_gateway,
        )

        result = service.chat("stu_001", "which backend")

        self.assertEqual(model_gateway.get_calls, ["deepseek"])
        self.assertEqual(gateway_backend.calls[0][:2], ("system", "which backend"))
        self.assertEqual(llm_service.calls, [])
        self.assertEqual(result["reply"], "gateway-answer")

    def test_chat_falls_back_to_original_profile_when_update_fails(self):
        profile = self.make_profile()
        db = StubDatabase(profile=profile)
        llm_service = StubLLMService(reply="answer")
        profile_agent = StubProfileAgent(error=RuntimeError("update failed"))
        history_service = StubChatHistoryService()
        prompt_service = StubChatPromptService()
        service = ChatService(db, llm_service, profile_agent, history_service, prompt_service)

        result = service.chat("stu_001", "explain neural networks")

        self.assertEqual(result["reply"], "answer")
        self.assertEqual(result["profile"]["name"], "test-user")
        self.assertEqual(db.saved_profiles, [])
        self.assertEqual(
            history_service.append_calls,
            [("stu_001", "explain neural networks", "answer")],
        )

    def test_chat_raises_404_when_profile_missing(self):
        service = ChatService(
            StubDatabase(profile=None),
            StubLLMService(),
            StubProfileAgent(),
            StubChatHistoryService(),
            StubChatPromptService(),
        )

        with self.assertRaises(HTTPException) as ctx:
            service.chat("stu_missing", "hello")

        self.assertEqual(ctx.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
