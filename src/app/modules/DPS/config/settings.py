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
    GOOGLE_API_KEY: str = Field(..., description="Gemini API key")
    CLIENT_PORTFOLIO_SOURCE_PATH: str = Field(
        default="",
        description="Optional path to the client portfolio CSV source file",
    )
    HNW_SEGMENT_MIN_AUM_AED: float = Field(
        10_000_000,
        description="Minimum total AUM in AED required to classify a client as HNW",
    )
    ELASTICSEARCH_URL: str = Field(..., description="Elastic Search endpoint")
    REALTIME_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent realtime workflow executions")
    STANDARD_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent standard workflow executions")
    GENERATE_INSIGHT_CONCURRENCY: int = Field(1, description="Concurrent generate insight executions")

settings = Settings()
