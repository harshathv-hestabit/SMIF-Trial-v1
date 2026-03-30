from pydantic import Field
from app.common.azure_services.settings import AzureServiceEmulatorSettings


class Settings(AzureServiceEmulatorSettings):
    GROQ_BASE_URL: str = Field(..., description="Groq API base URL")
    GROQ_API_KEY: str = Field(..., description="Groq API key")
    LLM_POOL_CONFIG: str = Field(
        default="",
        description="JSON array describing the LLM backend pool",
    )
    LLM_MAX_RETRIES: int = Field(3, description="Retries after pool exhaustion")
    LLM_TEMPERATURE: float = Field(0.3, description="Default LLM temperature")
    REALTIME_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent realtime workflow executions")
    STANDARD_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent standard workflow executions")
    STANDARD_WORKFLOW_BATCH_LIMIT: int = Field(50, description="Maximum delayed news items processed per standard workflow run")
    GENERATE_INSIGHT_CONCURRENCY: int = Field(1, description="Concurrent generate insight executions")

    GOOGLE_API_KEY: str = Field(..., description="Gemini API Key")
    ELASTICSEARCH_URL: str = Field(..., description="Elastic Search Endpoint")

settings = Settings()
