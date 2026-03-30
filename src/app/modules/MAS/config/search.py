from collections import defaultdict
import math

from elasticsearch import Elasticsearch
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from .settings import settings


INDEX = "clients"
DIM = 384
EMBEDDING_MODEL = "models/gemini-embedding-2-preview"

es = Elasticsearch(settings.ELASTICSEARCH_URL, verify_certs=False)
query_embedder = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    api_key=settings.GOOGLE_API_KEY,
    task_type="RETRIEVAL_QUERY",
    output_dimensionality=DIM,
)


def _normalize_embedding(vector: list[float]) -> list[float]:
    magnitude = math.sqrt(sum(value * value for value in vector))
    if not magnitude:
        return vector
    return [value / magnitude for value in vector]


def _embed_query(text: str) -> list[float]:
    return _normalize_embedding(query_embedder.embed_query(text))


def _news_to_text(doc: dict) -> str:
    return " ".join(
        filter(
            None,
            [
                doc.get("title", ""),
                doc.get("content", ""),
                " ".join(doc.get("tags", [])),
                " ".join(doc.get("symbols", [])),
            ],
        )
    )


def score_news_against_clients(
    news_doc: dict,
    top_k: int = 5,
    min_score: float = 0.0,
    client_segments: list[str] | None = None,
) -> list[dict]:
    news_text = _news_to_text(news_doc)
    news_vec = _embed_query(news_text)
    news_tags = [tag.upper() for tag in news_doc.get("tags", [])]
    news_tickers = [symbol.split(".")[0].upper() for symbol in news_doc.get("symbols", [])]
    segment_filter = _build_client_segment_filter(client_segments)

    knn_query: dict = {
        "field": "embedding",
        "query_vector": news_vec,
        "k": top_k,
        "num_candidates": 100,
    }
    if segment_filter:
        knn_query["filter"] = segment_filter

    knn_response = es.search(
        index=INDEX,
        size=top_k,
        knn=knn_query,
        source={"excludes": ["embedding"]},
    )

    bm25_query: dict = {
        "bool": {
            "should": [
                {"terms": {"ticker_symbols": news_tickers, "boost": 3.0}},
                {"terms": {"tags_of_interest": news_tags, "boost": 1.5}},
                {"match": {"asset_descriptions": {"query": news_text, "boost": 1.0}}},
                {"match": {"query": {"query": news_text, "boost": 0.8}}},
            ],
            "minimum_should_match": 1,
        }
    }
    if segment_filter:
        bm25_query["bool"]["filter"] = [segment_filter]

    bm25_response = es.search(
        index=INDEX,
        size=top_k,
        query=bm25_query,
        source={"excludes": ["embedding"]},
    )

    rrf_k = 60
    rrf_scores: dict[str, float] = defaultdict(float)
    hit_sources: dict[str, dict] = {}

    for rank, hit in enumerate(knn_response["hits"]["hits"], start=1):
        client_id = hit["_source"]["client_id"]
        rrf_scores[client_id] += 1 / (rrf_k + rank)
        hit_sources[client_id] = hit["_source"]

    for rank, hit in enumerate(bm25_response["hits"]["hits"], start=1):
        client_id = hit["_source"]["client_id"]
        rrf_scores[client_id] += 1 / (rrf_k + rank)
        hit_sources.setdefault(client_id, hit["_source"])

    max_rrf = max(rrf_scores.values(), default=1.0)
    results = []
    for client_id, raw_score in sorted(rrf_scores.items(), key=lambda item: -item[1]):
        normalized_score = round(raw_score / max_rrf, 4)
        if normalized_score < min_score:
            continue

        source = hit_sources[client_id]
        client_tickers = [ticker.upper() for ticker in source.get("ticker_symbols", [])]
        client_tags = [tag.upper() for tag in source.get("tags_of_interest", [])]
        results.append(
            {
                "client_id": client_id,
                "client_name": source["client_name"],
                "relevance_score": normalized_score,
                "matched_isins": list(set(client_tickers) & set(news_tickers)),
                "matched_tags": list(set(client_tags) & set(news_tags)),
                "matched_classifications": source.get("asset_classifications", []),
                "classification_weights": source.get("classification_weights", {}),
                "client_portfolio_document": source,
            }
        )

        if len(results) >= top_k:
            break

    return results


def process_news_stream(
    news_docs: list[dict],
    top_k: int = 5,
    min_score: float = 0.0,
    client_segments: list[str] | None = None,
) -> dict[str, list[dict]]:
    results = {}
    for doc in news_docs:
        news_id = doc.get("id", doc.get("title", "unknown"))
        matched_clients = score_news_against_clients(
            doc,
            top_k=top_k,
            min_score=min_score,
            client_segments=client_segments,
        )
        if matched_clients:
            results[news_id] = matched_clients
    return results


def _build_client_segment_filter(client_segments: list[str] | None) -> dict | None:
    normalized = sorted(
        {
            str(segment).strip().lower()
            for segment in (client_segments or [])
            if str(segment).strip()
        }
    )
    if not normalized:
        return None
    return {"terms": {"client_segment": normalized}}
