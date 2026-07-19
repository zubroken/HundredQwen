from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException


class PptService:
    VALID_DETAIL_LEVELS = {"brief", "standard", "detailed"}

    def __init__(self, zhiwen_service: Any):
        self.zhiwen_service = zhiwen_service

    def list_themes(self) -> Dict[str, Any]:
        return {
            "themes": self.zhiwen_service.get_themes(),
            "configured": self.zhiwen_service.configured,
        }

    def create_ppt(
        self,
        query: str,
        theme: str = "auto",
        detail_level: str = "standard",
    ) -> Dict[str, str]:
        if not self.zhiwen_service.configured:
            raise HTTPException(
                status_code=503,
                detail="讯飞智文服务未配置，请设置 ZHIWEN_APP_ID 和 ZHIWEN_APP_SECRET 环境变量",
            )

        normalized_detail_level = (
            detail_level if detail_level in self.VALID_DETAIL_LEVELS else "standard"
        )
        sid = self.zhiwen_service.create_ppt(
            query=query,
            theme=theme,
            detail_level=normalized_detail_level,
        )
        if not sid:
            raise HTTPException(status_code=500, detail="PPT创建失败，请检查日志")

        return {"sid": sid, "message": "PPT任务已创建"}

    def get_progress(self, sid: str) -> Dict[str, Any]:
        if not self.zhiwen_service.configured:
            return {"process": 0, "pptUrl": None, "errMsg": "讯飞智文服务未配置"}
        return self.zhiwen_service.get_progress(sid)
