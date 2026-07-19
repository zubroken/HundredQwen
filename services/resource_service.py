from __future__ import annotations

from models.resources import ResourceDB


class ResourceService:
    def __init__(self, resource_db: ResourceDB):
        self.resource_db = resource_db

    def list_resources(self, student_id: str, resource_type: str | None = None) -> dict:
        resources = self.resource_db.get_resources_by_student(student_id, resource_type)
        return {"resources": [resource.to_dict() for resource in resources]}

    def list_paths(self, student_id: str) -> dict:
        paths = self.resource_db.get_paths_by_student(student_id)
        return {"paths": [path.to_dict() for path in paths]}
