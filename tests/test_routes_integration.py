import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.routes import create_app
from services.llm_service import LLMConfig


class StubChatService:
    def __init__(self):
        self.calls = []

    def chat(self, student_id, message, model="deepseek", effort="high"):
        self.calls.append((student_id, message, model, effort))
        return {"reply": "stub-reply", "profile": {"student_id": student_id}}


class StubKnowledgeService:
    def __init__(self):
        self.search_calls = []

    def search(self, query, type_filter="all", doc_id="", include_arxiv=False):
        self.search_calls.append((query, type_filter, doc_id, include_arxiv))
        return {
            "query": query,
            "local": {"results": []},
            "arxiv": [],
            "documents": [],
        }


class StubPptService:
    def __init__(self):
        self.create_calls = []

    def create_ppt(self, query, theme="auto", detail_level="standard"):
        self.create_calls.append((query, theme, detail_level))
        return {"sid": "sid-001", "message": "PPT任务已创建"}


class StubUpdateLLMService:
    def __init__(self):
        self.calls = []

    def __call__(self, config):
        self.calls.append(config)


class StubUpdateLLMConfig:
    def __init__(self):
        self.calls = []

    def __call__(self, api_key="", model="", base_url=""):
        self.calls.append(
            {
                "api_key": api_key,
                "model": model,
                "base_url": base_url,
            }
        )
        return {"message": f"LLM配置已更新: {model or 'old-model'}"}


class StubResourceService:
    def __init__(self):
        self.resource_calls = []
        self.path_calls = []

    def list_resources(self, student_id, resource_type=None):
        self.resource_calls.append((student_id, resource_type))
        return {
            "resources": [
                {
                    "resource_id": "res-1",
                    "student_id": student_id,
                    "resource_type": resource_type or "document",
                }
            ]
        }

    def list_paths(self, student_id):
        self.path_calls.append(student_id)
        return {
            "paths": [
                {
                    "path_id": "path-1",
                    "student_id": student_id,
                }
            ]
        }


class StubGenerationService:
    def generate_bundle(self, request):
        return {
            "bundle_id": "bundle-1",
            "student_id": request["student_id"],
            "status": "completed",
            "resources": [],
            "path": {"path_id": "path-1", "nodes": []},
            "citations": [],
            "safety": {"risk_level": "low"},
            "warnings": [],
        }

    def list_bundles(self, student_id):
        return [{"bundle_id": "bundle-1", "student_id": student_id}]

    def get_learning_path(self, student_id):
        return {"path_id": "path-1", "student_id": student_id, "nodes": []}

    def update_path_node(self, path_id, node_id, status):
        return {"path_id": path_id, "nodes": [{"node_id": node_id, "status": status}]}


class RoutesIntegrationTest(unittest.TestCase):
    def make_services(self):
        return SimpleNamespace(
            account_service=SimpleNamespace(),
            chat_service=StubChatService(),
            exercise_service=SimpleNamespace(),
            knowledge_service=StubKnowledgeService(),
            ppt_service=StubPptService(),
            resource_service=StubResourceService(),
            generation_service=StubGenerationService(),
            llm_service=SimpleNamespace(
                config=LLMConfig(
                    api_key="old-key",
                    model="old-model",
                    base_url="https://old",
                )
            ),
            update_llm_service=StubUpdateLLMService(),
            update_llm_config=StubUpdateLLMConfig(),
        )

    def create_client(self, services):
        with patch("api.routes.build_app_services", return_value=services):
            return TestClient(
                create_app(LLMConfig(api_key="", model="deepseek-chat", base_url=""))
            )

    def test_root_returns_html(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("/api/chat-simple", response.text)

    def test_create_app_registers_expected_route_paths(self):
        services = self.make_services()

        with patch("api.routes.build_app_services", return_value=services):
            app = create_app(LLMConfig(api_key="", model="deepseek-chat", base_url=""))

        route_paths = {route.path for route in app.routes}
        self.assertTrue(
            {
                "/",
                "/api/login",
                "/api/register",
                "/api/profile/update",
                "/api/account/{student_id}",
                "/api/chat",
                "/api/chat-simple",
                "/api/exercise/generate",
                "/api/profile/{student_id}",
                "/api/resources/{student_id}",
                "/api/paths/{student_id}",
                "/api/generation/resource-bundle",
                "/api/generation/resource-bundles/{student_id}",
                "/api/generation/learning-path/{student_id}",
                "/api/generation/learning-path/{path_id}/nodes/{node_id}",
                "/api/config/llm",
                "/api/zhiwen/themes",
                "/api/zhiwen/ppt/create",
                "/api/zhiwen/ppt/progress",
                "/api/knowledge/documents",
                "/api/knowledge/search",
                "/api/knowledge/export",
                "/api/knowledge/stats",
            }.issubset(route_paths)
        )

    def test_create_app_uses_split_route_registrars_without_changing_behavior(self):
        services = self.make_services()

        with patch("api.routes.build_app_services", return_value=services):
            app = create_app(LLMConfig(api_key="", model="deepseek-chat", base_url=""))

        response = TestClient(app).post(
            "/api/chat-simple",
            json={"student_id": "stu_001", "message": "继续测试"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["reply"], "stub-reply")
        self.assertEqual(services.chat_service.calls[0][:2], ("stu_001", "继续测试"))

    def test_chat_simple_delegates_to_chat_service(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.post(
            "/api/chat-simple",
            json={"student_id": "stu_001", "message": "你好"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["reply"], "stub-reply")
        self.assertEqual(services.chat_service.calls[0][:2], ("stu_001", "你好"))

    def test_chat_simple_preserves_http_exception_status_and_detail(self):
        services = self.make_services()
        client = self.create_client(services)

        def raise_not_found(student_id, message, model="deepseek", effort="high"):
            raise HTTPException(status_code=404, detail="学生画像未找到")

        services.chat_service.chat = raise_not_found

        response = client.post(
            "/api/chat-simple",
            json={"student_id": "stu_missing", "message": "你好"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "学生画像未找到"})

    def test_knowledge_search_delegates_with_request_shape(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.post(
            "/api/knowledge/search",
            json={
                "query": "Transformer",
                "type_filter": "paper",
                "doc_id": "doc-1",
                "include_arxiv": True,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["query"], "Transformer")
        self.assertEqual(
            services.knowledge_service.search_calls,
            [("Transformer", "paper", "doc-1", True)],
        )

    def test_zhiwen_create_maps_legacy_page_count_before_service_call(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.post(
            "/api/zhiwen/ppt/create",
            json={"query": "机器学习导论", "theme": "auto", "page_count": 12},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sid"], "sid-001")
        self.assertEqual(
            services.ppt_service.create_calls,
            [("机器学习导论", "auto", "detailed")],
        )

    def test_zhiwen_create_maps_legacy_page_count_boundaries(self):
        services = self.make_services()
        client = self.create_client(services)

        client.post("/api/zhiwen/ppt/create", json={"query": "q1", "page_count": 4})
        client.post("/api/zhiwen/ppt/create", json={"query": "q2", "page_count": 7})
        client.post("/api/zhiwen/ppt/create", json={"query": "q3", "page_count": 8})
        client.post(
            "/api/zhiwen/ppt/create",
            json={"query": "q4", "page_count": 4, "detail_level": "detailed"},
        )

        self.assertEqual(
            services.ppt_service.create_calls,
            [
                ("q1", "auto", "brief"),
                ("q2", "auto", "standard"),
                ("q3", "auto", "detailed"),
                ("q4", "auto", "detailed"),
            ],
        )

    def test_update_llm_config_preserves_old_values_for_blank_fields(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.put(
            "/api/config/llm",
            json={"api_key": "", "model": "deepseek-chat", "base_url": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "LLM配置已更新: deepseek-chat")
        self.assertEqual(
            services.update_llm_config.calls,
            [
                {
                    "api_key": "",
                    "model": "deepseek-chat",
                    "base_url": "",
                }
            ],
        )
        self.assertEqual(services.update_llm_service.calls, [])

    def test_update_llm_config_returns_without_touching_legacy_rebind_path(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.put(
            "/api/config/llm",
            json={"api_key": "new-key", "model": "deepseek-reasoner", "base_url": "https://new"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "LLM配置已更新: deepseek-reasoner")
        self.assertEqual(
            services.update_llm_config.calls,
            [
                {
                    "api_key": "new-key",
                    "model": "deepseek-reasoner",
                    "base_url": "https://new",
                }
            ],
        )
        self.assertEqual(services.update_llm_service.calls, [])

    def test_get_resources_delegates_to_resource_service(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.get("/api/resources/stu_001", params={"resource_type": "document"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "resources": [
                    {
                        "resource_id": "res-1",
                        "student_id": "stu_001",
                        "resource_type": "document",
                    }
                ]
            },
        )
        self.assertEqual(
            services.resource_service.resource_calls,
            [("stu_001", "document")],
        )

    def test_get_paths_delegates_to_resource_service(self):
        services = self.make_services()
        client = self.create_client(services)

        response = client.get("/api/paths/stu_001")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "paths": [
                    {
                        "path_id": "path-1",
                        "student_id": "stu_001",
                    }
                ]
            },
        )
        self.assertEqual(services.resource_service.path_calls, ["stu_001"])


if __name__ == "__main__":
    unittest.main()
