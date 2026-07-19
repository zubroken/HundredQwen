import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.routes import create_app
from services.llm_service import LLMConfig


class StubGenerationService:
    def __init__(self):
        self.generate_calls = []
        self.update_calls = []

    def generate_bundle(self, request):
        self.generate_calls.append(request)
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
        self.update_calls.append((path_id, node_id, status))
        return {"path_id": path_id, "nodes": [{"node_id": node_id, "status": status}]}


class GenerationRoutesTest(unittest.TestCase):
    def make_client(self, service=None):
        service = service or StubGenerationService()
        services = SimpleNamespace(
            account_service=SimpleNamespace(),
            chat_service=SimpleNamespace(),
            exercise_service=SimpleNamespace(),
            knowledge_service=SimpleNamespace(),
            ppt_service=SimpleNamespace(),
            resource_service=SimpleNamespace(),
            generation_service=service,
            llm_service=SimpleNamespace(config=LLMConfig()),
            update_llm_config=lambda **kwargs: {},
        )
        with patch("api.routes.build_app_services", return_value=services):
            return TestClient(create_app(LLMConfig())), service

    def test_generate_resource_bundle_delegates_to_service(self):
        client, service = self.make_client()

        response = client.post(
            "/api/generation/resource-bundle",
            json={"student_id": "stu_001", "topic": "Transformer attention"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["bundle_id"], "bundle-1")
        self.assertEqual(service.generate_calls[0]["resource_types"][0], "document")

    def test_invalid_resource_type_returns_422(self):
        client, _ = self.make_client()

        response = client.post(
            "/api/generation/resource-bundle",
            json={
                "student_id": "stu_001",
                "topic": "Transformer attention",
                "resource_types": ["video"],
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_service_http_exception_status_is_preserved(self):
        class BlockingService(StubGenerationService):
            def generate_bundle(self, request):
                raise HTTPException(status_code=400, detail="blocked input")

        client, _ = self.make_client(BlockingService())

        response = client.post(
            "/api/generation/resource-bundle",
            json={"student_id": "stu_001", "topic": "blocked"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "blocked input"})

    def test_read_and_update_learning_path(self):
        client, service = self.make_client()

        list_response = client.get("/api/generation/resource-bundles/stu_001")
        path_response = client.get("/api/generation/learning-path/stu_001")
        update_response = client.put(
            "/api/generation/learning-path/path-1/nodes/node-1",
            json={"status": "completed"},
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(path_response.json()["path_id"], "path-1")
        self.assertEqual(update_response.json()["nodes"][0]["status"], "completed")
        self.assertEqual(service.update_calls, [("path-1", "node-1", "completed")])


if __name__ == "__main__":
    unittest.main()
