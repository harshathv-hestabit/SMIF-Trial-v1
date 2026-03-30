from pydantic import Field
from app.common.azure_services.settings import AzureServiceEmulatorSettings


class Settings(AzureServiceEmulatorSettings):
    GROQ_BASE_URL: str = Field(..., description="Groq API base URL")
    GROQ_API_KEY: str = Field(..., description="Groq API key")
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
