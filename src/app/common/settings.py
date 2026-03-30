from pydantic import Field
from app.common.azure_services.settings import AzureServiceEmulatorSettings


class Settings(AzureServiceEmulatorSettings):
    GROQ_BASE_URL: str = Field(..., description="Groq API base URL")
    GROQ_API_KEY: str = Field(..., description="Groq API key")
    REALTIME_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent realtime workflow executions")
    STANDARD_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent standard workflow executions")
    GENERATE_INSIGHT_CONCURRENCY: int = Field(1, description="Concurrent generate insight executions")
    BENZINGA_API_KEY: str = Field(..., description="BENZINGA API key")

settings = Settings()
