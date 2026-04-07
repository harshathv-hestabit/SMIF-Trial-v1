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
    LLM_POOL_CONFIG: str = Field(
        default="",
        description="JSON array describing the LLM backend pool",
    )
    LLM_MAX_RETRIES: int = Field(3, description="Retries after pool exhaustion")
    LLM_TEMPERATURE: float = Field(0.3, description="Default LLM temperature")
    MAX_COMPLETION_TOKENS: int = Field(300, description="Token limits for inference")
    
    REALTIME_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent realtime workflow executions")
    STANDARD_WORKFLOW_CONCURRENCY: int = Field(1, description="Concurrent standard workflow executions")
    STANDARD_WORKFLOW_BATCH_LIMIT: int = Field(50, description="Maximum delayed news items processed per standard workflow run")
    GENERATE_INSIGHT_CONCURRENCY: int = Field(1, description="Concurrent generate insight executions")
    SERVICEBUS_MAX_LOCK_RENEWAL_SECONDS: int = Field(
        900,
        description="Maximum lock renewal duration for long-running message handlers",
    )

    GOOGLE_API_KEY: str = Field(..., description="Gemini API Key")
    ELASTICSEARCH_URL: str = Field(..., description="Elastic Search Endpoint")
    RELEVANCE_RETRIEVAL_K: int = Field(
        10,
        description="Default hybrid retrieval depth before final candidate selection",
    )
    RELEVANCE_FINAL_TOP_N: int = Field(
        10,
        description="Default final number of selected clients per news item",
    )
    RELEVANCE_MIN_SCORE: float = Field(
        0.75,
        description="Minimum hybrid score required for structured-match candidates",
    )
    RELEVANCE_SEMANTIC_ONLY_MIN_SCORE: float = Field(
        0.55,
        description="Higher minimum score for semantic-only candidates without direct structured overlap",
    )
    RELEVANCE_PREFILTER_SCAN_LIMIT: int = Field(
        250,
        description="Maximum client documents scanned for deterministic prefiltering",
    )
    HNW_RELEVANCE_RETRIEVAL_K: int = Field(
        12,
        description="Hybrid retrieval depth for HNW candidate selection",
    )
    HNW_RELEVANCE_FINAL_TOP_N: int = Field(
        5,
        description="Default HNW final candidate cap for non-broad news",
    )
    HNW_RELEVANCE_BROAD_TOP_N: int = Field(
        5,
        description="HNW final candidate cap for broad macro or regulatory news",
    )
    HNW_RELEVANCE_MIN_SCORE: float = Field(
        0.85,
        description="Minimum hybrid score for HNW structured-match candidates",
    )
    EXECUTION_ROUTE_INDIRECT_MIN_TOP_MATCH_SCORE: float = Field(
        0.48,
        description="Minimum holdings-grounding top match score required for indirect single-pass insight generation",
    )
    EXECUTION_ROUTE_INDIRECT_MIN_MATCHED_HOLDINGS: int = Field(
        1,
        description="Minimum matched holdings required for indirect single-pass insight generation",
    )
    EXECUTION_ROUTE_SKIP_ON_SECURITY_TYPE_MISMATCH: bool = Field(
        True,
        description="Skip indirect generation when matched holdings conflict with inferred security type alignment",
    )

settings = Settings()
