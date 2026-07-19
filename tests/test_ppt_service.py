import unittest

from fastapi import HTTPException

from api.schemas import ZhiwenCreateRequest
from services.ppt_service import PptService


class StubZhiwenService:
    def __init__(self, configured=True, themes=None, sid="sid-123", progress=None):
        self.configured = configured
        self.themes = themes or [{"key": "auto", "name": "自动"}]
        self.sid = sid
        self.progress = progress or {"process": 70, "pptUrl": None, "errMsg": ""}
        self.create_calls = []
        self.progress_calls = []

    def get_themes(self):
        return self.themes

    def create_ppt(self, query, theme="auto", detail_level="standard"):
        self.create_calls.append((query, theme, detail_level))
        return self.sid

    def get_progress(self, sid):
        self.progress_calls.append(sid)
        return self.progress


class PptServiceTest(unittest.TestCase):
    def test_list_themes_returns_themes_and_configured_flag(self):
        zhiwen = StubZhiwenService(configured=False, themes=[{"key": "blue", "name": "蓝色"}])
        service = PptService(zhiwen)

        result = service.list_themes()

        self.assertEqual(
            result,
            {"themes": [{"key": "blue", "name": "蓝色"}], "configured": False},
        )

    def test_create_ppt_normalizes_invalid_detail_level_to_standard(self):
        zhiwen = StubZhiwenService(configured=True, sid="sid-001")
        service = PptService(zhiwen)

        result = service.create_ppt("机器学习导论", theme="auto", detail_level="invalid")

        self.assertEqual(result, {"sid": "sid-001", "message": "PPT任务已创建"})
        self.assertEqual(
            zhiwen.create_calls,
            [("机器学习导论", "auto", "standard")],
        )

    def test_create_ppt_raises_503_when_service_not_configured(self):
        service = PptService(StubZhiwenService(configured=False))

        with self.assertRaises(HTTPException) as ctx:
            service.create_ppt("机器学习导论")

        self.assertEqual(ctx.exception.status_code, 503)

    def test_create_ppt_raises_500_when_service_returns_empty_sid(self):
        service = PptService(StubZhiwenService(configured=True, sid=""))

        with self.assertRaises(HTTPException) as ctx:
            service.create_ppt("机器学习导论")

        self.assertEqual(ctx.exception.status_code, 500)

    def test_get_progress_returns_service_payload_when_not_configured(self):
        service = PptService(StubZhiwenService(configured=False))

        result = service.get_progress("sid-001")

        self.assertEqual(result, {"process": 0, "pptUrl": None, "errMsg": "讯飞智文服务未配置"})

    def test_get_progress_returns_service_payload(self):
        zhiwen = StubZhiwenService(
            configured=True,
            progress={"process": 100, "pptUrl": "http://example.com/a.pptx", "errMsg": ""},
        )
        service = PptService(zhiwen)

        result = service.get_progress("sid-001")

        self.assertEqual(zhiwen.progress_calls, ["sid-001"])
        self.assertEqual(
            result,
            {"process": 100, "pptUrl": "http://example.com/a.pptx", "errMsg": ""},
        )

    def test_create_ppt_accepts_legacy_page_count_mapping(self):
        req = ZhiwenCreateRequest.model_validate(
            {"query": "机器学习导论", "theme": "auto", "page_count": 12}
        )

        self.assertEqual(req.detail_level, "detailed")


if __name__ == "__main__":
    unittest.main()
