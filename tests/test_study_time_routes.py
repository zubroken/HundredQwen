import unittest
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.learning_routes import register_learning_routes


class FakeStudyTimeService:
    def __init__(self):
        self.calls = []

    def get_summary(self, student_id):
        self.calls.append(("summary", student_id))
        return {"student_id": student_id, "week_seconds": 93600, "active": False}

    def start(self, student_id):
        self.calls.append(("start", student_id))
        return {"student_id": student_id, "active": True}

    def pause(self, student_id):
        self.calls.append(("pause", student_id))
        return {"student_id": student_id, "week_seconds": 93600, "active": False}

    end = pause


class StudyTimeRoutesTest(unittest.TestCase):
    def test_study_time_routes_delegate_to_service(self):
        service = FakeStudyTimeService()
        app = FastAPI()
        register_learning_routes(app, SimpleNamespace(study_time_service=service))
        client = TestClient(app)

        self.assertEqual(client.get("/api/study-time/stu_001").json()["week_seconds"], 93600)
        self.assertTrue(client.post("/api/study-time/stu_001/start").json()["active"])
        self.assertFalse(client.post("/api/study-time/stu_001/pause").json()["active"])
        self.assertEqual(
            service.calls,
            [("summary", "stu_001"), ("start", "stu_001"), ("pause", "stu_001")],
        )


if __name__ == "__main__":
    unittest.main()
