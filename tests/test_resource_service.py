import unittest

from models.resources import LearningPath, PathNode, Resource
from services.resource_service import ResourceService


class StubResourceDB:
    def __init__(self):
        self.resource_calls = []
        self.path_calls = []

    def get_resources_by_student(self, student_id, resource_type=None):
        self.resource_calls.append((student_id, resource_type))
        return [
            Resource(
                resource_id="res-1",
                title="Intro",
                student_id=student_id,
                resource_type=resource_type or "document",
            )
        ]

    def get_paths_by_student(self, student_id):
        self.path_calls.append(student_id)
        return [
            LearningPath(
                path_id="path-1",
                student_id=student_id,
                title="AI Path",
                nodes=[PathNode(node_id="node-1", title="Basics")],
            )
        ]


class ResourceServiceTest(unittest.TestCase):
    def setUp(self):
        self.resource_db = StubResourceDB()
        self.service = ResourceService(self.resource_db)

    def test_list_resources_serializes_resource_models(self):
        result = self.service.list_resources("stu_001", "document")

        self.assertEqual(self.resource_db.resource_calls, [("stu_001", "document")])
        self.assertEqual(
            result,
            {
                "resources": [
                    {
                        "resource_id": "res-1",
                        "title": "Intro",
                        "resource_type": "document",
                        "content": {},
                        "tags": [],
                        "difficulty": "intermediate",
                        "course_name": "",
                        "created_at": "",
                        "student_id": "stu_001",
                    }
                ]
            },
        )

    def test_list_paths_serializes_learning_path_models(self):
        result = self.service.list_paths("stu_001")

        self.assertEqual(self.resource_db.path_calls, ["stu_001"])
        self.assertEqual(
            result,
            {
                "paths": [
                    {
                        "path_id": "path-1",
                        "student_id": "stu_001",
                        "course_name": "",
                        "title": "AI Path",
                        "description": "",
                        "nodes": [
                            {
                                "node_id": "node-1",
                                "title": "Basics",
                                "description": "",
                                "resource_ids": [],
                                "estimated_hours": 1.0,
                                "prerequisites": [],
                                "status": "pending",
                                "order": 0,
                            }
                        ],
                        "total_estimated_hours": 0.0,
                        "difficulty": "intermediate",
                        "created_at": "",
                        "updated_at": "",
                        "status": "active",
                    }
                ]
            },
        )


if __name__ == "__main__":
    unittest.main()
