"""
多智能体个性化学习系统 v1.0.4 —— 主程序入口（DeepSeek + 讯飞星火）

启动方式：
  python main.py                    # 启动 Web 服务（默认 DeepSeek）
  python main.py --model deepseek-chat --port 8000
"""
from __future__ import annotations
import argparse
import logging
import os
import sys

from dotenv import load_dotenv
from settings import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9010


def resolve_port(cli_port: int | None, env: dict[str, str] | None = None) -> int:
    """命令行端口优先；未指定时才读取环境变量。"""
    if cli_port is not None:
        return cli_port

    configured_port = (env or os.environ).get("SERVER_PORT", str(DEFAULT_PORT))
    try:
        port = int(configured_port)
    except ValueError as exc:
        raise ValueError("SERVER_PORT 必须是 1 到 65535 的整数") from exc

    if not 1 <= port <= 65535:
        raise ValueError("SERVER_PORT 必须是 1 到 65535 的整数")
    return port


def run_server(args):
    """启动 Web 服务"""
    try:
        import uvicorn
    except ImportError:
        logger.error("需要安装 uvicorn: pip install uvicorn")
        sys.exit(1)

    from services.database import init_db
    init_db()
    from services.llm_service import LLMConfig
    from api.routes import create_app

    llm_config = LLMConfig(
        api_key=args.api_key or os.getenv("DEEPSEEK_API_KEY", ""),
        model=args.model or "deepseek-chat",
    )

    app = create_app(llm_config)
    try:
        port = resolve_port(args.port)
    except ValueError as exc:
        logger.error(str(exc))
        sys.exit(2)

    logger.info(f"启动 Web 服务: http://localhost:{port}")
    logger.info(f"版本: v1.0.4")
    logger.info(f"LLM: DeepSeek, 模型: {args.model}")
    logger.info(f"可用接口:")
    logger.info(f"  POST /api/login          - 登录验证")
    logger.info(f"  POST /api/chat-simple    - 智能问答（纯文本对话）")
    logger.info(f"  POST /api/exercise/generate - 练习题生成")
    logger.info(f"  POST /api/chat           - 对话式画像构建")
    logger.info(f"  GET  /api/profile/       - 获取画像")
    logger.info(f"  PUT  /api/profile/update - 更新画像")
    logger.info(f"  PUT  /api/config/llm     - 更新LLM配置")

    uvicorn.run(app, host=args.host or DEFAULT_HOST, port=port)


def main():
    parser = argparse.ArgumentParser(description="多智能体个性化学习系统 v1.0.4")
    parser.add_argument("--api-key", help="DeepSeek API 密钥")
    parser.add_argument("--model", default="deepseek-chat", help="模型名称")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Web 服务监听地址")
    parser.add_argument("--port", type=int, default=None, help="Web 服务端口（默认读取 SERVER_PORT，未配置时为 9010）")

    args = parser.parse_args()
    run_server(args)


if __name__ == "__main__":
    main()
