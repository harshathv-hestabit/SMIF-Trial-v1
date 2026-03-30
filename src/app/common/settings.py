from pydantic import AliasChoices, Field
from app.common.azure_services.settings import AzureServiceEmulatorSettings


class Settings(AzureServiceEmulatorSettings):
    LLM_BASE_URL: str = Field(
        ...,
        description="OpenAI-compatible LLM API base URL",
        validation_alias=AliasChoices("LLM_BASE_URL", "GROQ_BASE_URL"),
    )
    LLM_API_KEY: str = Field(
        ...,
        description="OpenAI-compatible LLM API key",
        validation_alias=AliasChoices("LLM_API_KEY", "GROQ_API_KEY"),
    )
    REALTIME_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent realtime workflow executions")
    STANDARD_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent standard workflow executions")
    GENERATE_INSIGHT_CONCURRENCY: int = Field(1, description="Concurrent generate insight executions")
    BENZINGA_API_KEY: str = Field(..., description="BENZINGA API key")

settings = Settings()
