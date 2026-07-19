import unittest

from services.model_gateway import ModelGateway, ModelGatewayConfig


class StubBackend:
    def __init__(self, name, available=True):
        self.name = name
        self.available = available

    def chat(self, system_prompt, user_message, temperature=None):
        return f"{self.name}:{user_message}"

    def chat_json(self, system_prompt, user_message, temperature=None):
        return {"backend": self.name, "message": user_message}


class ModelGatewayTest(unittest.TestCase):
    def test_from_config_builds_gateway_with_default_backend(self):
        deepseek = StubBackend("deepseek")
        spark = StubBackend("spark")
        config = ModelGatewayConfig(
            default_backend="deepseek",
            backends={"deepseek": deepseek, "spark": spark},
        )

        gateway = ModelGateway.from_config(config)

        self.assertIs(gateway.get(), deepseek)
        self.assertIs(gateway.get("spark"), spark)

    def test_get_returns_default_backend_when_name_missing(self):
        deepseek = StubBackend("deepseek")
        spark = StubBackend("spark")
        gateway = ModelGateway(default_backend="deepseek", backends={"deepseek": deepseek, "spark": spark})

        self.assertIs(gateway.get(), deepseek)
        self.assertIs(gateway.get("spark"), spark)

    def test_list_backends_exposes_registered_backend_names_and_availability(self):
        gateway = ModelGateway(
            default_backend="deepseek",
            backends={
                "deepseek": StubBackend("deepseek", available=True),
                "spark": StubBackend("spark", available=False),
            },
        )

        self.assertEqual(
            gateway.list_backends(),
            {
                "deepseek": {"available": True, "is_default": True},
                "spark": {"available": False, "is_default": False},
            },
        )

    def test_set_default_requires_registered_backend(self):
        gateway = ModelGateway(default_backend="deepseek", backends={"deepseek": StubBackend("deepseek")})

        gateway.set_default("deepseek")

        with self.assertRaises(KeyError):
            gateway.set_default("spark")

    def test_get_status_includes_default_backend_and_availability(self):
        gateway = ModelGateway(
            default_backend="deepseek",
            backends={
                "deepseek": StubBackend("deepseek", available=True),
                "spark": StubBackend("spark", available=False),
            },
        )

        status = gateway.get_status()

        self.assertEqual(status["default_backend"], "deepseek")
        self.assertEqual(
            status["backends"],
            {
                "deepseek": {"available": True, "is_default": True},
                "spark": {"available": False, "is_default": False},
            },
        )

    def test_get_status_preserves_list_backends_contract(self):
        gateway = ModelGateway(
            default_backend="deepseek",
            backends={
                "deepseek": StubBackend("deepseek", available=True),
                "spark": StubBackend("spark", available=False),
            },
        )

        self.assertEqual(gateway.list_backends(), gateway.get_status()["backends"])


if __name__ == "__main__":
    unittest.main()
