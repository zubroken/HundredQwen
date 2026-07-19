from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, TypeVar

from agents.code_example_agent import CodeExampleAgent
from agents.document_agent import DocumentAgent
from agents.exercise_agent import ExerciseAgent
from agents.learning_path_agent import LearningPathAgent
from agents.mindmap_agent import MindMapAgent
from agents.orchestrator import Orchestrator
from agents.profile_agent import ProfileAgent
from agents.reading_agent import ReadingAgent
from models.resources import ResourceDB
from services.account_service import AccountService
from services.chat_history_service import ChatHistoryService
from services.chat_prompt_service import ChatPromptService
from services.chat_service import ChatService
from services.database import DatabaseManager
from services.document_service import DocumentService
from services.docx_exporter import DocxExporter
from services.exercise_service import ExerciseService
from services.knowledge_base import KnowledgeBase
from services.knowledge_service import KnowledgeService
from services.llm_service import LLMConfig, LLMService
from services.model_gateway import ModelGateway, ModelGatewayConfig
from services.paper_fetcher import PaperFetcher
from services.ppt_service import PptService
from services.resource_service import ResourceService
from services.skill_tree_service import SkillTreeService
from services.speech_service import SpeechService
from services.study_time_service import StudyTimeService
from services.spark_service import SparkConfig, SparkService
from services.zhiwen_service import ZhiwenService

AgentT = TypeVar("AgentT")


@dataclass
class AppServices:
    llm_service: LLMService
    db: DatabaseManager
    account_service: AccountService
    orchestrator: Orchestrator
    agents: List[object]
    resource_db: ResourceDB
    resource_service: ResourceService
    model_gateway: ModelGateway
    zhiwen_service: ZhiwenService
    ppt_service: PptService
    spark_service: SparkService
    knowledge_base: KnowledgeBase
    paper_fetcher: PaperFetcher
    docx_exporter: DocxExporter
    knowledge_service: KnowledgeService
    chat_history_service: ChatHistoryService
    chat_prompt_service: ChatPromptService
    chat_service: ChatService
    exercise_service: ExerciseService
    document_service: DocumentService
    profile_agent: ProfileAgent
    document_agent: DocumentAgent
    mindmap_agent: MindMapAgent
    reading_agent: ReadingAgent
    code_example_agent: CodeExampleAgent
    learning_path_agent: LearningPathAgent
    exercise_agent: ExerciseAgent
    skill_tree_service: SkillTreeService
    speech_service: SpeechService
    study_time_service: StudyTimeService

    def get_model_gateway_status(self) -> dict:
        return self.model_gateway.get_status()

    def update_llm_config(self, api_key: str = "", model: str = "", base_url: str = "") -> dict:
        updated_config = LLMConfig(
            api_key=api_key or self.llm_service.config.api_key,
            model=model or self.llm_service.config.model,
            base_url=base_url or self.llm_service.config.base_url,
        )
        self.update_llm_service(updated_config)
        return {"message": f"LLM配置已更新: {updated_config.model}"}

    def update_llm_service(self, llm_config: LLMConfig) -> None:
        self.llm_service = LLMService(llm_config)
        self._rebind_llm_consumers()

    def _rebind_llm_consumers(self) -> None:
        self.model_gateway.backends["deepseek"] = self.llm_service
        self.orchestrator.llm = self.llm_service
        self.chat_service.llm_service = self.llm_service

        for agent in self.agents:
            agent.llm = self.llm_service


def _build_agents_and_orchestrator(
    llm_service: LLMService,
) -> tuple[ProfileAgent, ExerciseAgent, list[object], Orchestrator]:
    profile_agent = ProfileAgent(llm_service)
    document_agent = DocumentAgent(llm_service)
    mindmap_agent = MindMapAgent(llm_service)
    exercise_agent = ExerciseAgent(llm_service)
    reading_agent = ReadingAgent(llm_service)
    code_example_agent = CodeExampleAgent(llm_service)
    learning_path_agent = LearningPathAgent(llm_service)

    orchestrator = Orchestrator(llm_service)
    agents = [
        profile_agent,
        document_agent,
        mindmap_agent,
        exercise_agent,
        reading_agent,
        code_example_agent,
        learning_path_agent,
    ]
    for agent in agents:
        orchestrator.register_agent(agent)

    return profile_agent, exercise_agent, agents, orchestrator


def _build_zhiwen_service_from_env(env: dict[str, str] | None = None) -> ZhiwenService:
    env = env or os.environ
    return ZhiwenService(
        app_id=env.get("ZHIWEN_APP_ID", ""),
        app_secret=env.get("ZHIWEN_APP_SECRET", ""),
    )


def _build_spark_config_from_env(env: dict[str, str] | None = None) -> SparkConfig:
    env = env or os.environ
    return SparkConfig(
        api_key=env.get("SPARK_API_KEY", ""),
        model=env.get("SPARK_MODEL", "lite"),
    )


def _build_spark_service_from_env(env: dict[str, str] | None = None) -> SparkService:
    return SparkService(_build_spark_config_from_env(env))


def _build_model_gateway_config(
    llm_service: LLMService,
    spark_service: SparkService,
) -> ModelGatewayConfig:
    return ModelGatewayConfig(
        default_backend="deepseek",
        backends={
            "deepseek": llm_service,
            "spark": spark_service,
        },
    )


def _build_model_gateway(llm_service: LLMService, spark_service: SparkService) -> ModelGateway:
    return ModelGateway.from_config(_build_model_gateway_config(llm_service, spark_service))


def _bind_model_gateway_to_agents(model_gateway: ModelGateway, agents: list[object]) -> None:
    for agent in agents:
        if hasattr(agent, "model_gateway"):
            agent.model_gateway = model_gateway


def _find_agent(agents: list[object], agent_type: type[AgentT]) -> AgentT:
    for agent in agents:
        if isinstance(agent, agent_type):
            return agent
    raise LookupError(f"Agent not found: {agent_type.__name__}")


def _build_content_services() -> tuple[
    ResourceDB,
    ResourceService,
    ZhiwenService,
    PptService,
    SparkService,
    KnowledgeBase,
    PaperFetcher,
    DocxExporter,
    KnowledgeService,
]:
    resource_db = ResourceDB()
    resource_service = ResourceService(resource_db)

    zhiwen_service = _build_zhiwen_service_from_env()
    ppt_service = PptService(zhiwen_service)
    spark_service = _build_spark_service_from_env()

    knowledge_base = KnowledgeBase()
    paper_fetcher = PaperFetcher()
    docx_exporter = DocxExporter()
    knowledge_service = KnowledgeService(knowledge_base, paper_fetcher, docx_exporter)

    return (
        resource_db,
        resource_service,
        zhiwen_service,
        ppt_service,
        spark_service,
        knowledge_base,
        paper_fetcher,
        docx_exporter,
        knowledge_service,
    )


def _build_feature_services(
    db: DatabaseManager,
    llm_service: LLMService,
    profile_agent: ProfileAgent,
    exercise_agent: ExerciseAgent,
    knowledge_base: KnowledgeBase,
    model_gateway: ModelGateway,
) -> tuple[
    ChatHistoryService,
    ChatPromptService,
    ChatService,
    ExerciseService,
    AccountService,
]:
    chat_history_service = ChatHistoryService()
    chat_prompt_service = ChatPromptService(knowledge_base)
    chat_service = ChatService(
        db=db,
        llm_service=llm_service,
        profile_agent=profile_agent,
        chat_history_service=chat_history_service,
        chat_prompt_service=chat_prompt_service,
        model_gateway=model_gateway,
    )
    exercise_service = ExerciseService(
        db=db,
        knowledge_base=knowledge_base,
        exercise_agent=exercise_agent,
    )
    account_service = AccountService(db, profile_agent)

    return (
        chat_history_service,
        chat_prompt_service,
        chat_service,
        exercise_service,
        account_service,
    )


def build_app_services(llm_config: LLMConfig | None = None) -> AppServices:
    llm_service = LLMService(llm_config or LLMConfig())
    db = DatabaseManager()

    profile_agent, exercise_agent, agents, orchestrator = _build_agents_and_orchestrator(llm_service)
    document_agent = _find_agent(agents, DocumentAgent)
    mindmap_agent = _find_agent(agents, MindMapAgent)
    reading_agent = _find_agent(agents, ReadingAgent)
    code_example_agent = _find_agent(agents, CodeExampleAgent)
    learning_path_agent = _find_agent(agents, LearningPathAgent)
    (
        resource_db,
        resource_service,
        zhiwen_service,
        ppt_service,
        spark_service,
        knowledge_base,
        paper_fetcher,
        docx_exporter,
        knowledge_service,
    ) = _build_content_services()
    model_gateway = _build_model_gateway(llm_service, spark_service)
    _bind_model_gateway_to_agents(model_gateway, agents)
    (
        chat_history_service,
        chat_prompt_service,
        chat_service,
        exercise_service,
        account_service,
    ) = _build_feature_services(
        db=db,
        llm_service=llm_service,
        profile_agent=profile_agent,
        exercise_agent=exercise_agent,
        knowledge_base=knowledge_base,
        model_gateway=model_gateway,
    )

    document_service = DocumentService(
        db=db,
        document_agent=document_agent,
        knowledge_base=knowledge_base,
    )

    return AppServices(
        llm_service=llm_service,
        db=db,
        account_service=account_service,
        orchestrator=orchestrator,
        agents=agents,
        resource_db=resource_db,
        resource_service=resource_service,
        model_gateway=model_gateway,
        zhiwen_service=zhiwen_service,
        ppt_service=ppt_service,
        spark_service=spark_service,
        knowledge_base=knowledge_base,
        paper_fetcher=paper_fetcher,
        docx_exporter=docx_exporter,
        knowledge_service=knowledge_service,
        chat_history_service=chat_history_service,
        chat_prompt_service=chat_prompt_service,
        chat_service=chat_service,
        exercise_service=exercise_service,
        document_service=document_service,
        profile_agent=profile_agent,
        document_agent=document_agent,
        mindmap_agent=mindmap_agent,
        reading_agent=reading_agent,
        code_example_agent=code_example_agent,
        learning_path_agent=learning_path_agent,
        exercise_agent=exercise_agent,
        skill_tree_service=SkillTreeService(db, llm_service),
        speech_service=SpeechService(
            app_id=os.environ.get("SPARK_APP_ID", ""),
            api_key=os.environ.get("SPARK_API_KEY", ""),
            api_secret=os.environ.get("SPARK_API_SECRET", ""),
        ),
        study_time_service=StudyTimeService(),
    )
