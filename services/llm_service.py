"""
LLM 服务层 —— DeepSeek / Spark 大模型统一调用接口
为多智能体系统提供统一的模型调用接口
"""
from __future__ import annotations
import os
import json
import logging
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    api_key: str = ""
    model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com/v1"
    temperature: float = 0.7
    max_tokens: int = 4096


class BaseLLMClient:
    """LLM 客户端基类：OpenAI 兼容接口的通用实现"""

    def __init__(self):
        self.client = None

    # ---- 子类需覆盖的钩子 ----

    def _get_api_key(self) -> str:
        raise NotImplementedError

    def _get_base_url(self) -> str:
        raise NotImplementedError

    def _get_model_name(self) -> str:
        raise NotImplementedError

    def _get_service_label(self) -> str:
        raise NotImplementedError

    # ---- 通用实现 ----

    def _init_client(self):
        api_key = self._get_api_key()
        base_url = self._get_base_url()

        if not api_key:
            logger.warning(f"未配置 {self._get_service_label()} API Key")
            return

        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self._chat_model = self._get_model_name()
            logger.info(f"{self._get_service_label()} 客户端已初始化 (模型: {self._chat_model})")
        except ImportError:
            logger.error("openai 包未安装，请执行: pip install openai")
        except Exception as e:
            logger.error(f"初始化 {self._get_service_label()} 客户端失败: {e}")

    @property
    def available(self) -> bool:
        return self.client is not None

    def chat(self, system_prompt: str, user_message: str,
             temperature: Optional[float] = None) -> str:
        """统一的聊天接口"""
        if not self.client:
            return json.dumps({
                "message": f"[错误] {self._get_service_label()} 客户端未初始化，请检查 API Key 配置",
                "request_preview": user_message[:100]
            }, ensure_ascii=False)

        try:
            resp = self.client.chat.completions.create(
                model=self._chat_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature or self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"{self._get_service_label()} 调用失败: {e}")
            return f"[错误: {e}]"

    def chat_json(self, system_prompt: str, user_message: str,
                  temperature: Optional[float] = None) -> dict:
        """返回 JSON 的聊天调用"""
        from utils.helpers import safe_json_parse
        response = self.chat(system_prompt, user_message, temperature)
        result = safe_json_parse(response)
        if result is None:
            logger.warning(f"解析 {self._get_service_label()} 返回的 JSON 失败: {response[:200]}")
            return {"error": "parse_failed", "raw": response}
        return result


class LLMService(BaseLLMClient):
    """DeepSeek LLM 服务，通过 OpenAI 兼容接口调用"""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        super().__init__()
        self._init_client()

    def _get_api_key(self) -> str:
        return self.config.api_key or os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY") or ""

    def _get_base_url(self) -> str:
        return self.config.base_url or os.getenv("DEEPSEEK_BASE_URL") or os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")

    def _get_model_name(self) -> str:
        return self.config.model

    def _get_service_label(self) -> str:
        return "DeepSeek"
