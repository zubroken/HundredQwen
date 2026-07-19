from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ModelGatewayConfig:
    default_backend: str
    backends: dict[str, object]


class ModelGateway:
    def __init__(self, default_backend: str, backends: dict[str, object]):
        if default_backend not in backends:
            raise KeyError(f"Unknown default backend: {default_backend}")
        self.default_backend = default_backend
        self.backends = backends

    @classmethod
    def from_config(cls, config: ModelGatewayConfig) -> "ModelGateway":
        return cls(
            default_backend=config.default_backend,
            backends=config.backends,
        )

    def get(self, name: str | None = None) -> object:
        backend_name = name or self.default_backend
        return self.backends[backend_name]

    def set_default(self, name: str) -> None:
        if name not in self.backends:
            raise KeyError(f"Unknown backend: {name}")
        self.default_backend = name

    def get_status(self) -> dict:
        """只读状态快照：
        区分'已注册' / '运行时可用' / '当前默认后端' / '可外部切换'
        - available: 运行时可用
        - is_default: 当前默认后端
        当前 Spark 仅结构注册，非业务默认路径"""
        return {
            "default_backend": self.default_backend,
            "backends": {
                name: {
                    "available": bool(getattr(backend, "available", True)),
                    "is_default": name == self.default_backend,
                }
                for name, backend in self.backends.items()
            },
        }

    def list_backends(self) -> dict[str, dict[str, bool]]:
        """向后兼容：仅返回后端可用性映射"""
        return self.get_status()["backends"]
