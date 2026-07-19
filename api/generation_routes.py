from __future__ import annotations

from fastapi import FastAPI, HTTPException

from api.schemas import PathNodeStatusRequest, ResourceBundleRequest
from services.app_services import AppServices


def register_generation_routes(app: FastAPI, services: AppServices) -> None:
    @app.post("/api/generation/resource-bundle")
    async def generate_resource_bundle(req: ResourceBundleRequest):
        try:
            return services.generation_service.generate_bundle(req.model_dump())
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    @app.get("/api/generation/resource-bundles/{student_id}")
    async def list_resource_bundles(student_id: str):
        return {"bundles": services.generation_service.list_bundles(student_id)}

    @app.get("/api/generation/learning-path/{student_id}")
    async def get_learning_path(student_id: str):
        path = services.generation_service.get_learning_path(student_id)
        if not path:
            raise HTTPException(status_code=404, detail="learning path not found")
        return path

    @app.put("/api/generation/learning-path/{path_id}/nodes/{node_id}")
    async def update_learning_path_node(path_id: str, node_id: str, req: PathNodeStatusRequest):
        return services.generation_service.update_path_node(path_id, node_id, req.status)
