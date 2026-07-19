"""
讯飞智文 PPT 生成服务
基于讯飞智文 API：https://zwapi.xfyun.cn/api/aippt

功能：获取免费模板、创建PPT任务、查询生成进度
"""
from __future__ import annotations
import hashlib
import hmac
import base64
import time
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)


class ZhiwenService:
    """讯飞智文 PPT 生成服务"""

    BASE_URL = "https://zwapi.xfyun.cn/api/aippt"

    # 免费内置模板列表（fallback，API 不通时使用）
    BUILTIN_THEMES = [
        {"key": "purple", "name": "紫影幽蓝", "thumbnail": "", "free": True},
        {"key": "green", "name": "清新绿意", "thumbnail": "", "free": True},
        {"key": "lightblue", "name": "清逸天蓝", "thumbnail": "", "free": True},
        {"key": "taupe", "name": "质感之境", "thumbnail": "", "free": True},
        {"key": "blue", "name": "星光夜影", "thumbnail": "", "free": True},
        {"key": "telecomRed", "name": "炽热暖阳", "thumbnail": "", "free": True},
        {"key": "telecomGreen", "name": "幻翠奇旅", "thumbnail": "", "free": True},
    ]

    def __init__(self, app_id: str = "", app_secret: str = ""):
        self.app_id = app_id
        self.app_secret = app_secret

    @property
    def configured(self) -> bool:
        return bool(self.app_id and self.app_secret)

    def _sign(self) -> dict:
        """生成讯飞智文鉴权头"""
        ts = int(time.time())
        auth_str = hashlib.md5(f"{self.app_id}{ts}".encode()).hexdigest()
        signature = base64.b64encode(
            hmac.new(self.app_secret.encode(), auth_str.encode(), hashlib.sha1).digest()
        ).decode()
        return {
            "appId": self.app_id,
            "timestamp": str(ts),
            "signature": signature,
        }

    def get_themes(self) -> list:
        """获取可用主题列表，优先从API获取，失败则返回内置模板"""
        if not self.configured:
            logger.info("智文未配置凭证，返回内置模板列表")
            return self.BUILTIN_THEMES

        try:
            headers = self._sign()
            resp = requests.get(f"{self.BASE_URL}/themeList", headers=headers, timeout=10)
            data = resp.json()
            if data.get("flag") and data.get("code") == 0:
                themes = data.get("data", [])
                for t in themes:
                    t["free"] = True
                logger.info(f"获取到 {len(themes)} 个主题")
                return themes
            logger.warning(f"获取主题列表失败: {data.get('desc', 'unknown')}")
        except Exception as e:
            logger.warning(f"获取主题列表异常: {e}")

        return self.BUILTIN_THEMES

    # 内容详细度 → prompt 映射
    DETAIL_PROMPTS = {
        "brief": "简洁版，内容精炼概括，3-4个主要章节，突出核心要点即可",
        "standard": "标准版，内容适中，5-7个主要章节，兼顾深度与广度",
        "detailed": "详尽版，内容全面深入，8-10个主要章节，覆盖知识体系全貌",
    }

    def create_ppt(
        self,
        query: str,
        theme: str = "auto",
        detail_level: str = "standard",
    ) -> Optional[str]:
        """创建PPT生成任务

        Args:
            query: PPT 主题/要求（最多8000字）
            theme: 模板主题 key
            detail_level: 内容详细度 brief / standard / detailed

        Returns:
            sid (任务ID) 或 None
        """
        if not self.configured:
            return None

        detail_hint = self.DETAIL_PROMPTS.get(detail_level, self.DETAIL_PROMPTS["standard"])
        enhanced_query = f"请生成一个关于「{query}」的PPT演示文稿，{detail_hint}。"

        payload = {
            "query": enhanced_query[:8000],
            "create_model": "auto",
            "theme": theme,
            "is_card_note": False,
            "is_cover_img": True,
            "is_figure": True,
            "language": "cn",
        }

        try:
            headers = {**self._sign(), "Content-Type": "application/json"}
            resp = requests.post(
                f"{self.BASE_URL}/create", headers=headers, json=payload, timeout=30
            )
            data = resp.json()
            if data.get("code") == 0:
                sid = data.get("data", {}).get("sid")
                logger.info(f"PPT 任务创建成功: sid={sid}")
                return sid
            logger.error(f"创建 PPT 失败: code={data.get('code')} desc={data.get('desc')}")
            return None
        except Exception as e:
            logger.error(f"创建 PPT 异常: {e}")
            return None

    def get_progress(self, sid: str) -> dict:
        """查询 PPT 生成进度

        Returns:
            {"process": int, "pptUrl": str|None, "errMsg": str}
            process: 30=大纲完成, 70=PPT生成完成, 100=导出完成
        """
        if not self.configured or not sid:
            return {"process": 0, "pptUrl": None, "errMsg": "未配置凭证"}

        try:
            headers = self._sign()
            resp = requests.get(
                f"{self.BASE_URL}/progress", headers=headers, params={"sid": sid}, timeout=10
            )
            data = resp.json()
            if data.get("code") == 0:
                d = data.get("data", {})
                return {
                    "process": d.get("process", 0),
                    "pptId": d.get("pptId"),
                    "pptUrl": d.get("pptUrl"),
                    "errMsg": d.get("errMsg", ""),
                }
            return {"process": 0, "pptUrl": None, "errMsg": data.get("desc", "查询失败")}
        except Exception as e:
            logger.error(f"查询进度异常: {e}")
            return {"process": 0, "pptUrl": None, "errMsg": str(e)}
