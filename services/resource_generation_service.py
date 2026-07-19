from __future__ import annotations

import time

from fastapi import HTTPException

from models.resources import Resource, ResourceBundle
from services.citation_service import CitationService
from services.content_safety_service import ContentSafetyService
from utils.helpers import generate_id, now_str


class ResourceGenerationService:
    SUPPORTED_TYPES = ["document", "mindmap", "exercise", "reading", "code_example"]
    CORE_TYPES = {"document", "exercise"}

    def __init__(
        self,
        db,
        resource_db,
        knowledge_base,
        document_agent,
        mindmap_agent,
        exercise_agent,
        reading_agent,
        code_example_agent,
        learning_path_agent,
        safety_service: ContentSafetyService | None = None,
        citation_service: CitationService | None = None,
        agent_timeout_seconds: float = 30.0,
        monotonic_clock=None,
    ):
        self.db = db
        self.resource_db = resource_db
        self.knowledge_base = knowledge_base
        self.agents = {
            "document": (document_agent, "generate_document"),
            "mindmap": (mindmap_agent, "generate_mindmap"),
            "exercise": (exercise_agent, "generate_exercises"),
            "reading": (reading_agent, "generate_readings"),
            "code_example": (code_example_agent, "generate_code_example"),
        }
        self.learning_path_agent = learning_path_agent
        self.safety_service = safety_service or ContentSafetyService()
        self.citation_service = citation_service or CitationService()
        self.agent_timeout_seconds = agent_timeout_seconds
        self.monotonic_clock = monotonic_clock or time.monotonic

    def generate_bundle(self, request: dict) -> dict:
        student_id = request.get("student_id", "")
        profile = self.db.get_student(student_id)
        if not profile:
            raise HTTPException(status_code=404, detail="student not found")

        topic = request.get("topic", "")
        safety = self.safety_service.check_input(topic)
        if not safety.allowed:
            raise HTTPException(status_code=400, detail=safety.reason)

        resource_types = request.get("resource_types") or list(self.SUPPORTED_TYPES)
        chunks = self.knowledge_base.retrieve(topic, top_k=5)
        citation_result = self.citation_service.from_chunks(chunks)
        warnings = list(citation_result["warnings"])
        prompt = self._build_agent_prompt(request, citation_result)

        resources_by_type: dict[str, Resource] = {}
        failed: list[str] = []
        agent_logs: list[dict] = []
        for resource_type in resource_types:
            agent, method_name = self.agents[resource_type]
            agent_name = getattr(agent, "name", agent.__class__.__name__)
            started_at = self.monotonic_clock()
            duration_ms = 0
            agent_status = "completed"
            try:
                resource = getattr(agent, method_name)(profile, prompt)
                duration_ms = round((self.monotonic_clock() - started_at) * 1000)
                if duration_ms > self.agent_timeout_seconds * 1000:
                    raise TimeoutError(
                        f"{agent_name} timed out after {duration_ms}ms "
                        f"(limit {round(self.agent_timeout_seconds * 1000)}ms)"
                    )
                resource.student_id = student_id
                resource.course_name = request.get("course_name", "")
                resource.difficulty = request.get("difficulty", "intermediate")
                resource.citations = citation_result["citations"]
                resource.evidence_level = citation_result["evidence_level"]
                output_check = self.safety_service.check_output(str(resource.content))
                if not output_check.allowed:
                    raise ValueError(output_check.reason)
                self.resource_db.save_resource(resource)
                resources_by_type[resource_type] = resource
            except Exception as exc:
                failed.append(resource_type)
                warnings.append(f"{resource_type} generation failed: {exc}")
                agent_status = "fallback"
                if not duration_ms:
                    duration_ms = round((self.monotonic_clock() - started_at) * 1000)
                resource = self._fallback_resource(
                    resource_type=resource_type,
                    profile=profile,
                    request=request,
                    citation_result=citation_result,
                    reason=str(exc),
                )
                self.resource_db.save_resource(resource)
                resources_by_type[resource_type] = resource
            agent_logs.append(
                {
                    "agent_name": agent_name,
                    "duration_ms": duration_ms,
                    "status": agent_status,
                    "warning_count": len(warnings),
                }
            )

        if not resources_by_type:
            raise HTTPException(status_code=502, detail="resource generation failed")

        path = self.learning_path_agent.generate_path(profile, resources_by_type)
        path.course_name = request.get("course_name", "")
        self.resource_db.save_path(path)

        status = "partial" if failed else "completed"
        bundle = ResourceBundle(
            bundle_id=generate_id("bundle"),
            student_id=student_id,
            topic=topic,
            course_name=request.get("course_name", ""),
            resource_ids=[resource.resource_id for resource in resources_by_type.values()],
            path_id=path.path_id,
            citations=citation_result["citations"],
            safety={"risk_level": safety.risk_level, "reason": safety.reason},
            status=status,
            created_at=now_str(),
            warnings=warnings,
        )
        self.resource_db.save_bundle(bundle)
        response = self._expand_bundle(bundle.to_dict(), resources_by_type.values(), path)
        response["agent_logs"] = agent_logs
        return response

    def list_bundles(self, student_id: str) -> list[dict]:
        bundles = self.resource_db.get_bundles_by_student(student_id)
        resources = {
            r.resource_id: r.to_dict()
            for r in self.resource_db.get_resources_by_student(student_id)
        }
        paths = {
            p.path_id: p.to_dict()
            for p in self.resource_db.get_paths_by_student(student_id)
        }
        for bundle in bundles:
            bundle["resources"] = [
                resources[resource_id]
                for resource_id in bundle.get("resource_ids", [])
                if resource_id in resources
            ]
            bundle["path"] = paths.get(bundle.get("path_id"))
        return bundles

    def get_learning_path(self, student_id: str) -> dict | None:
        paths = self.resource_db.get_paths_by_student(student_id)
        if not paths:
            return None
        return paths[-1].to_dict()

    def update_path_node(self, path_id: str, node_id: str, status: str) -> dict:
        if status not in {"pending", "in_progress", "completed"}:
            raise HTTPException(status_code=422, detail="invalid node status")
        path = self.resource_db.get_path_by_id(path_id)
        if not path:
            raise HTTPException(status_code=404, detail="learning path not found")
        for node in path.nodes:
            if node.node_id == node_id:
                node.status = status
                path.updated_at = now_str()
                self.resource_db.save_path(path)
                return path.to_dict()
        raise HTTPException(status_code=404, detail="learning path node not found")

    def _build_agent_prompt(self, request: dict, citation_result: dict) -> str:
        lines = [
            f"Course: {request.get('course_name', '')}",
            f"Topic: {request.get('topic', '')}",
            f"Difficulty: {request.get('difficulty', 'intermediate')}",
            f"Evidence: {citation_result['evidence_level']}",
        ]
        for item in citation_result["citations"]:
            lines.append(f"- {item['title']} p.{item['page']}: {item['snippet']}")
        return "\n".join(lines)

    def _expand_bundle(self, bundle: dict, resources, path) -> dict:
        bundle["resources"] = [resource.to_dict() for resource in resources]
        bundle["path"] = path.to_dict()
        return bundle

    def _fallback_resource(self, resource_type: str, profile, request: dict, citation_result: dict, reason: str) -> Resource:
        citations = citation_result["citations"]
        snippet = citations[0]["snippet"] if citations else "Knowledge base evidence is insufficient; please verify."
        title = {
            "document": "Fallback explanation document",
            "mindmap": "Fallback mindmap outline",
            "exercise": "Fallback practice set",
            "reading": "Fallback reading guide",
            "code_example": "Fallback code example",
        }.get(resource_type, "Fallback resource")
        content = {
            "summary": f"Generated from local knowledge because model generation failed: {reason}",
            "key_points": [snippet],
            "evidence_level": citation_result["evidence_level"],
        }
        if resource_type == "exercise":
            content["questions"] = [
                {
                    "stem": f"Explain the main idea from this evidence: {snippet}",
                    "answer": "Use the cited material to describe the concept in your own words.",
                    "explanation": snippet,
                }
            ]
        if resource_type == "code_example":
            content["language"] = "Python"
            content["code"] = "# fallback example\nprint('Study the cited Transformer attention evidence first')"
        return Resource(
            resource_id=generate_id(resource_type.replace("_example", "")),
            title=title,
            resource_type=resource_type,
            content=content,
            tags=[request.get("topic", "")],
            difficulty=request.get("difficulty", "intermediate"),
            course_name=request.get("course_name", ""),
            created_at=now_str(),
            student_id=profile.student_id,
            citations=citations,
            evidence_level=citation_result["evidence_level"],
            fallback=True,
        )
