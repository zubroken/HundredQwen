"""
讯飞星火（Spark）大模型服务
通过 OpenAI 兼容接口调用星火模型（Spark Lite / Max / X2 等）

模型版本通过 .env 中的 SPARK_MODEL 控制，随时可切换：
  SPARK_MODEL=lite        # Spark Lite（轻量快速）
  SPARK_MODEL=max         # Spark Max（专业级）
  SPARK_MODEL=x2          # Spark X2（旗舰）

API 地址：https://spark-api-open.xfyun.cn/v1
"""
from __future__ import annotations
import os
import logging
from typing import Optional
from dataclasses import dataclass

from services.llm_service import BaseLLMClient

logger = logging.getLogger(__name__)

# Spark 模型版本 → API 模型名映射
SPARK_MODEL_MAP = {
    "lite": "spark-lite",
    "max": "spark-max",
    "x2": "spark-x2",
    "x2-flash": "spark-x2-flash",
}


@dataclass
class SparkConfig:
    api_key: str = ""
    api_secret: str = ""
    app_id: str = ""
    model: str = "lite"  # lite / max / x2 / x2-flash
    base_url: str = "https://spark-api-open.xfyun.cn/v1"
    temperature: float = 0.7
    max_tokens: int = 4096


class SparkService(BaseLLMClient):
    """讯飞星火 LLM 服务（OpenAI 兼容接口）"""

    def __init__(self, config: Optional[SparkConfig] = None):
        self.config = config or SparkConfig()
        super().__init__()
        self._init_client()

    def _get_api_key(self) -> str:
        return self.config.api_key or os.getenv("SPARK_API_KEY", "")

    def _get_base_url(self) -> str:
        return self.config.base_url

    def _get_model_name(self) -> str:
        return SPARK_MODEL_MAP.get(self.config.model, self.config.model)

    def _get_service_label(self) -> str:
        return "Spark"
