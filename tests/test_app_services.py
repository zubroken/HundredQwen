import unittest
from unittest.mock import patch

from services.app_services import (
    _build_agents_and_orchestrator,
    _build_model_gateway_config,
    _build_model_gateway,
    _build_spark_config_from_env,
    _build_zhiwen_service_from_env,
    build_app_services,
)
from services.llm_service import LLMConfig
from services.llm_service import LLMService


class AppServicesTest(unittest.TestCase):
    def test_build_model_gateway_config_registers_default_and_backends(self):
        services = build_app_services(LLMConfig(api_key="", model="deepseek-chat", base_url=""))

        config = _build_model_gateway_config(services.llm_service, services.spark_service)

        self.assertEqual(config.default_backend, "deepseek")
        self.assertIs(config.backends["deepseek"], services.llm_service)
        self.assertIs(config.backends["spark"], services.spark_service)

    def test_build_model_gateway_registers_deepseek_and_spark(self):
        services = build_app_services(LLMConfig(api_key="", model="deepseek-chat", base_url=""))

        gateway = _build_model_gateway(services.llm_service, services.spark_service)

        self.assertIs(gateway.get("deepseek"), services.llm_service)
        self.assertIs(gateway.get("spark"), services.spark_service)
        self.assertIs(gateway.get(), services.llm_service)

    def test_build_zhiwen_service_reads_credentials_from_env(self):
        service = _build_zhiwen_service_from_env(
            {
                "ZHIWEN_APP_ID": "zhiwen-app-id",
                "ZHIWEN_APP_SECRET": "zhiwen-app-secret",
            }
        )

        self.assertEqual(service.app_id, "zhiwen-app-id")
        self.assertEqual(service.app_secret, "zhiwen-app-secret")

    def test_build_spark_config_reads_values_from_env(self):
        config = _build_spark_config_from_env(
            {
                "SPARK_API_KEY": "spark-key",
                "SPARK_MODEL": "x2",
            }
        )

        self.assertEqual(config.api_key, "spark-key")
        self.assertEqual(config.model, "x2")

    def test_build_agents_and_orchestrator_registers_all_agents(self):
        llm_service = LLMService(LLMConfig(api_key="", model="deepseek-chat", base_url=""))

        profile_agent, exercise_agent, agents, orchestrator = _build_agents_and_orchestrator(llm_service)

        self.assertIs(profile_agent, agents[0])
        self.assertIs(exercise_agent, agents[3])
        self.assertEqual(len(agents), 7)
        self.assertIs(orchestrator.llm, llm_service)
        self.assertEqual(len(orchestrator.agents), len(agents))

    def test_build_app_services_wires_shared_dependencies(self):
        services = build_app_services(LLMConfig(api_key="", model="deepseek-chat", base_url=""))

        self.assertIs(services.account_service.db, services.db)
        self.assertIs(services.chat_service.db, services.db)
        self.assertIs(services.exercise_service.db, services.db)
        self.assertIs(services.chat_service.llm_service, services.llm_service)
        self.assertIs(services.chat_service.chat_prompt_service.knowledge_base, services.knowledge_base)
        self.assertIs(services.exercise_service.knowledge_base, services.knowledge_base)
        self.assertIs(services.knowledge_service.knowledge_base, services.knowledge_base)
        self.assertIs(services.resource_service.resource_db, services.resource_db)
        self.assertIs(services.generation_service.db, services.db)
        self.assertIs(services.generation_service.resource_db, services.resource_db)
        self.assertIs(services.generation_service.knowledge_base, services.knowledge_base)
        self.assertIs(
            services.generation_service.agents["document"][0],
            services.document_agent,
        )
        self.assertIs(
            services.generation_service.learning_path_agent,
            services.learning_path_agent,
        )
        self.assertIs(services.ppt_service.zhiwen_service, services.zhiwen_service)
        self.assertIs(services.model_gateway.get("deepseek"), services.llm_service)
        self.assertIs(services.model_gateway.get("spark"), services.spark_service)
        self.assertIs(services.profile_agent.model_gateway, services.model_gateway)
        self.assertIs(services.exercise_agent.model_gateway, services.model_gateway)
        self.assertIs(services.document_agent.model_gateway, services.model_gateway)
        self.assertIs(services.mindmap_agent.model_gateway, services.model_gateway)
        self.assertIs(services.reading_agent.model_gateway, services.model_gateway)
        self.assertIs(services.code_example_agent.model_gateway, services.model_gateway)
        self.assertIs(services.learning_path_agent.model_gateway, services.model_gateway)
        self.assertIs(services.profile_agent, services.agents[0])

    def test_update_llm_service_rebinds_all_llm_consumers(self):
        services = build_app_services(LLMConfig(api_key="", model="deepseek-chat", base_url=""))
        old_llm = services.llm_service

        services.update_llm_service(
            LLMConfig(api_key="new-key", model="deepseek-reasoner", base_url="https://example.com/v1")
        )

        self.assertIsNot(services.llm_service, old_llm)
        self.assertIs(services.chat_service.llm_service, services.llm_service)
        self.assertIs(services.account_service.profile_agent.llm, services.llm_service)
        self.assertIs(services.chat_service.profile_agent.llm, services.llm_service)
        self.assertIs(services.orchestrator.llm, services.llm_service)
        for agent in services.agents:
            self.assertIs(agent.llm, services.llm_service)

    def test_update_llm_config_merges_blank_fields_before_rebinding(self):
        services = build_app_services(
            LLMConfig(api_key="old-key", model="old-model", base_url="https://old")
        )

        with patch.object(services, "update_llm_service") as update_llm_service:
            result = services.update_llm_config(
                api_key="",
                model="deepseek-chat",
                base_url="",
            )

        update_llm_service.assert_called_once()
        updated = update_llm_service.call_args.args[0]
        self.assertEqual(updated.api_key, "old-key")
        self.assertEqual(updated.model, "deepseek-chat")
        self.assertEqual(updated.base_url, "https://old")
        self.assertEqual(result, {"message": "LLM配置已更新: deepseek-chat"})


if __name__ == "__main__":
    unittest.main()
