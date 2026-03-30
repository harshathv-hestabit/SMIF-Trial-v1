import math

from elasticsearch import Elasticsearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.modules.DPS.config.settings import settings


INDEX = "clients"
DIM = 384
EMBEDDING_MODEL = "models/gemini-embedding-2-preview"

INDEX_PROPERTIES = {
    "client_id": {"type": "keyword"},
    "client_name": {"type": "text"},
    "client_type": {"type": "keyword"},
    "client_segment": {"type": "keyword"},
    "client_segment_reason": {"type": "keyword"},
    "mandate": {"type": "keyword"},
    "total_aum_aed": {"type": "double"},
    "asset_types": {"type": "keyword"},
    "asset_subtypes": {"type": "keyword"},
    "asset_classifications": {"type": "keyword"},
    "currencies": {"type": "keyword"},
    "isins": {"type": "keyword"},
    "ticker_symbols": {"type": "keyword"},
    "asset_ids": {"type": "keyword"},
    "asset_descriptions": {"type": "text"},
    "classification_weights": {"type": "object", "enabled": False},
    "asset_type_weights": {"type": "object", "enabled": False},
    "query": {"type": "text"},
    "tags_of_interest": {"type": "keyword"},
    "embedding": {
        "type": "dense_vector",
        "dims": DIM,
        "index": True,
        "similarity": "cosine",
    },
}

es = Elasticsearch(settings.ELASTICSEARCH_URL, verify_certs=False)
document_embedder = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=settings.GOOGLE_API_KEY,
    task_type="RETRIEVAL_DOCUMENT",
    output_dimensionality=DIM,
)


def create_index() -> None:
    if es.indices.exists(index=INDEX).body:
        es.indices.put_mapping(index=INDEX, properties=INDEX_PROPERTIES)
        return

    es.indices.create(
        index=INDEX,
        settings={
            "number_of_shards": 1,
            "number_of_replicas": 0,
        },
        mappings={"properties": INDEX_PROPERTIES},
    )


def index_client_documents(documents: list[dict]) -> None:
    create_index()
    for document in documents:
        es.index(
            index=INDEX,
            id=document["client_id"],
            document={
                **document,
                "embedding": _embed_document(_client_document_to_text(document)),
            },
        )


def _normalize_embedding(vector: list[float]) -> list[float]:
    magnitude = math.sqrt(sum(value * value for value in vector))
    if not magnitude:
        return vector
    return [value / magnitude for value in vector]


def _embed_document(text: str) -> list[float]:
    return _normalize_embedding(document_embedder.embed_documents([text])[0])


def _client_document_to_text(document: dict) -> str:
    return " ".join(
        filter(
            None,
            [
                document.get("query", ""),
                " ".join(document.get("asset_classifications", [])),
                " ".join(document.get("asset_descriptions", [])[:20]),
                " ".join(document.get("currencies", [])),
                document.get("mandate", ""),
                document.get("client_type", ""),
            ],
        )
    )
