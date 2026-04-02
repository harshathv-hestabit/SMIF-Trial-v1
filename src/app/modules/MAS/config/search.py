from collections import defaultdict
import math
import re

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

CLASSIFICATION_TAG_MAP = {
    "EQUITIES": {
        "EQUITY MARKETS",
        "STOCK MARKET",
        "SHARE PRICE MOVEMENT",
        "IPO",
        "STOCK SPLIT",
        "BUYBACK",
        "DIVIDEND",
    },
    "FIXED INCOME": {
        "BOND MARKETS",
        "INTEREST RATE CHANGES",
        "CREDIT EVENTS",
        "YIELD CURVE",
        "BOND ISSUANCE",
        "DEFAULT RISK",
        "MATURITY",
        "COUPON",
        "FIXED INCOME",
        "DURATION RISK",
        "SPREAD WIDENING",
    },
    "REAL ESTATE": {
        "REAL ESTATE",
        "REIT",
        "PROPERTY MARKET",
        "DIVIDEND PAYMENTS",
        "RENTAL YIELD",
        "PROPERTY VALUATION",
    },
    "ALTERNATIVES": {
        "ALTERNATIVE INVESTMENTS",
        "STRUCTURED PRODUCTS",
        "HEDGE FUNDS",
        "VOLATILITY",
        "DERIVATIVES",
        "OPTIONS",
    },
    "COMMODITIES": {
        "COMMODITIES",
        "RAW MATERIALS",
        "ENERGY MARKETS",
        "METALS",
    },
    "MULTI ASSETS": {
        "MULTI-ASSET",
        "PORTFOLIO REBALANCING",
        "ASSET ALLOCATION",
    },
}
CLASSIFICATION_KEYWORDS = {
    "EQUITIES": ("equity", "stock", "shares", "equities"),
    "FIXED INCOME": ("bond", "yield", "coupon", "credit", "rate", "rates", "fixed income"),
    "REAL ESTATE": ("reit", "property", "real estate", "housing", "commercial real estate"),
    "ALTERNATIVES": ("hedge fund", "structured product", "option", "derivative", "volatility"),
    "COMMODITIES": ("commodity", "oil", "gold", "metals", "energy", "raw materials"),
    "MULTI ASSETS": ("multi asset", "asset allocation", "rebalancing", "portfolio"),
}
MANDATE_KEYWORDS = {
    "CONSERVATIVE": {"bond", "yield", "income", "rate", "rates", "credit", "defensive"},
    "BALANCED": {"macro", "allocation", "portfolio", "diversified", "diversification"},
    "AGGRESSIVE": {"growth", "equity", "stock", "technology", "ipo", "risk"},
    "INCOME": {"income", "yield", "coupon", "dividend"},
    "GROWTH": {"growth", "equity", "stock", "earnings", "technology"},
}
BROAD_MACRO_PATTERNS = (
    "central bank",
    "fed",
    "ecb",
    "boe",
    "boj",
    "pboc",
    "policy",
    "regulation",
    "regulatory",
    "sanction",
    "tariff",
    "inflation",
    "interest rate",
    "rates",
    "election",
    "government",
    "tax",
    "geopolitical",
    "macro",
    "recession",
)
TOKEN_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9&/+\-_.]{1,}")


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


def _normalize_keyword(value: object | None) -> str:
    text = str(value or "").strip().upper()
    if not text:
        return ""
    return re.sub(r"\s+", " ", text)


def _normalize_ticker(value: object | None) -> str:
    text = _normalize_keyword(value)
    if not text:
        return ""
    return text.split(".")[0]


def _tokenize_text(value: str) -> set[str]:
    return {match.group(0) for match in TOKEN_PATTERN.finditer(value.upper())}


def _extract_news_features(news_doc: dict) -> dict:
    title = str(news_doc.get("title") or "")
    content = str(news_doc.get("content") or "")
    topic_text = " ".join(part for part in [title, content] if part).strip()
    normalized_tags = sorted(
        {
            _normalize_keyword(tag)
            for tag in news_doc.get("tags", [])
            if _normalize_keyword(tag)
        }
    )
    normalized_tickers = sorted(
        {
            _normalize_ticker(symbol)
            for symbol in news_doc.get("symbols", [])
            if _normalize_ticker(symbol)
        }
    )
    inferred_classifications = set()
    upper_topic_text = topic_text.upper()
    for classification, tags in CLASSIFICATION_TAG_MAP.items():
        if set(normalized_tags) & tags:
            inferred_classifications.add(classification)
    for classification, keywords in CLASSIFICATION_KEYWORDS.items():
        if any(keyword.upper() in upper_topic_text for keyword in keywords):
            inferred_classifications.add(classification)
    return {
        "news_text": _news_to_text(news_doc),
        "topic_text": topic_text,
        "news_tags": normalized_tags,
        "news_tickers": normalized_tickers,
        "news_classifications": sorted(inferred_classifications),
        "broad_macro": _is_broad_macro_news(topic_text=topic_text, news_tags=normalized_tags),
    }


def _is_broad_macro_news(*, topic_text: str, news_tags: list[str]) -> bool:
    haystack = " ".join([topic_text.upper(), " ".join(news_tags)])
    return any(pattern.upper() in haystack for pattern in BROAD_MACRO_PATTERNS)


def _fetch_client_documents(
    *,
    client_segments: list[str] | None,
    size: int,
) -> list[dict]:
    segment_filter = _build_client_segment_filter(client_segments)
    query: dict = {"match_all": {}}
    if segment_filter:
        query = {"bool": {"filter": [segment_filter]}}
    response = es.search(
        index=INDEX,
        size=size,
        query=query,
        source={"excludes": ["embedding"]},
        sort=[{"client_id": "asc"}],
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]


def _build_prefilter_signal(client_doc: dict, news_features: dict) -> dict:
    client_tickers = {
        _normalize_ticker(ticker)
        for ticker in client_doc.get("ticker_symbols", [])
        if _normalize_ticker(ticker)
    }
    client_tags = {
        _normalize_keyword(tag)
        for tag in client_doc.get("tags_of_interest", [])
        if _normalize_keyword(tag)
    }
    client_classifications = {
        _normalize_keyword(classification)
        for classification in client_doc.get("asset_classifications", [])
        if _normalize_keyword(classification)
    }
    mandate_tokens = _tokenize_text(str(client_doc.get("mandate") or ""))
    topic_tokens = _tokenize_text(news_features["topic_text"])
    normalized_mandate = _normalize_keyword(client_doc.get("mandate"))
    matched_tickers = sorted(client_tickers & set(news_features["news_tickers"]))
    matched_tags = sorted(client_tags & set(news_features["news_tags"]))
    matched_classifications = sorted(
        client_classifications & set(news_features["news_classifications"])
    )

    has_mandate_fit = False
    if normalized_mandate:
        has_mandate_fit = bool(mandate_tokens & topic_tokens)
        for keyword in MANDATE_KEYWORDS.get(normalized_mandate, set()):
            if keyword.upper() in news_features["topic_text"].upper():
                has_mandate_fit = True
                break

    return {
        "client_id": client_doc["client_id"],
        "has_direct_ticker_match": bool(matched_tickers),
        "has_tag_overlap": bool(matched_tags),
        "has_classification_overlap": bool(matched_classifications),
        "has_mandate_fit": has_mandate_fit,
        "ticker_overlap_count": len(matched_tickers),
        "tag_overlap_count": len(matched_tags),
        "classification_overlap_count": len(matched_classifications),
        "matched_tickers": matched_tickers,
        "matched_tags": matched_tags,
        "matched_classifications": matched_classifications,
    }


def _prefilter_candidates(
    client_docs: list[dict],
    news_features: dict,
) -> tuple[dict[str, dict], list[str]]:
    signals_by_client: dict[str, dict] = {}
    eligible_ids: list[str] = []
    for client_doc in client_docs:
        signal = _build_prefilter_signal(client_doc, news_features)
        client_id = signal["client_id"]
        signals_by_client[client_id] = signal
        if (
            signal["has_direct_ticker_match"]
            or signal["has_tag_overlap"]
            or signal["has_classification_overlap"]
            or signal["has_mandate_fit"]
        ):
            eligible_ids.append(client_id)
    return signals_by_client, eligible_ids


def _compose_filter(
    segment_filter: dict | None,
    client_ids: list[str] | None = None,
) -> list[dict]:
    filters: list[dict] = []
    if segment_filter:
        filters.append(segment_filter)
    if client_ids:
        filters.append({"terms": {"client_id": client_ids}})
    return filters


def _build_bm25_query(news_features: dict, filters: list[dict]) -> dict:
    should: list[dict] = []
    if news_features["news_tickers"]:
        should.append(
            {"terms": {"ticker_symbols": news_features["news_tickers"], "boost": 8.0}}
        )
    if news_features["news_tags"]:
        should.append(
            {"terms": {"tags_of_interest": news_features["news_tags"], "boost": 5.0}}
        )
    if news_features["news_classifications"]:
        should.append(
            {
                "terms": {
                    "asset_classifications": news_features["news_classifications"],
                    "boost": 3.0,
                }
            }
        )
    if news_features["topic_text"]:
        should.extend(
            [
                {
                    "match": {
                        "asset_descriptions": {
                            "query": news_features["topic_text"],
                            "operator": "and",
                            "boost": 1.2,
                        }
                    }
                },
                {
                    "match": {
                        "query": {
                            "query": news_features["topic_text"],
                            "minimum_should_match": "70%",
                            "boost": 0.8,
                        }
                    }
                },
            ]
        )
    return {
        "bool": {
            "filter": filters,
            "should": should or [{"match_none": {}}],
            "minimum_should_match": 1,
        }
    }


def _run_hybrid_retrieval(
    *,
    news_features: dict,
    retrieval_k: int,
    segment_filter: dict | None,
    client_ids: list[str] | None,
) -> tuple[dict, dict]:
    filters = _compose_filter(segment_filter, client_ids)
    knn_query: dict = {
        "field": "embedding",
        "query_vector": _embed_query(news_features["news_text"]),
        "k": retrieval_k,
        "num_candidates": max(retrieval_k * 4, retrieval_k),
    }
    if filters:
        knn_query["filter"] = filters

    knn_response = es.search(
        index=INDEX,
        size=retrieval_k,
        knn=knn_query,
        source={"excludes": ["embedding"]},
    )
    bm25_response = es.search(
        index=INDEX,
        size=retrieval_k,
        query=_build_bm25_query(news_features, filters),
        source={"excludes": ["embedding"]},
    )
    return knn_response, bm25_response


def _build_selection_reason(signal: dict, score: float, semantic_only: bool) -> str:
    reasons: list[str] = []
    if signal["has_direct_ticker_match"]:
        reasons.append(f"ticker_overlap={signal['ticker_overlap_count']}")
    if signal["has_tag_overlap"]:
        reasons.append(f"tag_overlap={signal['tag_overlap_count']}")
    if signal["has_classification_overlap"]:
        reasons.append(
            f"classification_overlap={signal['classification_overlap_count']}"
        )
    if signal["has_mandate_fit"]:
        reasons.append("mandate_fit")
    if semantic_only:
        reasons.append("semantic_fallback")
    reasons.append(f"hybrid_rank_score={score:.4f}")
    return ", ".join(reasons)


def _dedupe_hits_by_client(hits: list[dict]) -> list[dict]:
    deduped: list[dict] = []
    seen: set[str] = set()
    for hit in hits:
        client_id = hit["_source"]["client_id"]
        if client_id in seen:
            continue
        seen.add(client_id)
        deduped.append(hit)
    return deduped


def score_news_against_clients(
    news_doc: dict,
    top_k: int | None = None,
    min_score: float | None = None,
    client_segments: list[str] | None = None,
    retrieval_k: int | None = None,
    final_top_n: int | None = None,
) -> list[dict]:
    """Return only candidates worth downstream generation to reduce token waste.

    Hybrid search is kept for ranking, but deterministic overlaps are used first to
    cheaply narrow the pool and semantic-only fallbacks are held to a stricter bar.
    """
    retrieval_limit = max(
        int(retrieval_k or top_k or settings.RELEVANCE_RETRIEVAL_K),
        1,
    )
    final_limit = max(
        int(final_top_n or top_k or settings.RELEVANCE_FINAL_TOP_N),
        1,
    )
    structured_min_score = (
        settings.RELEVANCE_MIN_SCORE if min_score is None else float(min_score)
    )
    semantic_only_min_score = max(
        float(settings.RELEVANCE_SEMANTIC_ONLY_MIN_SCORE),
        structured_min_score,
    )
    news_features = _extract_news_features(news_doc)
    segment_filter = _build_client_segment_filter(client_segments)
    client_docs = _fetch_client_documents(
        client_segments=client_segments,
        size=max(int(settings.RELEVANCE_PREFILTER_SCAN_LIMIT), retrieval_limit),
    )
    signals_by_client, prefiltered_ids = _prefilter_candidates(client_docs, news_features)
    broad_macro = news_features["broad_macro"]
    effective_retrieval_limit = min(
        max(retrieval_limit, len(prefiltered_ids)),
        max(int(settings.RELEVANCE_PREFILTER_SCAN_LIMIT), retrieval_limit),
    )

    primary_ids = prefiltered_ids or None
    knn_response, bm25_response = _run_hybrid_retrieval(
        news_features=news_features,
        retrieval_k=effective_retrieval_limit,
        segment_filter=segment_filter,
        client_ids=primary_ids,
    )

    fallback_knn_hits: list[dict] = []
    fallback_bm25_hits: list[dict] = []
    if broad_macro and prefiltered_ids:
        fallback_knn_response, fallback_bm25_response = _run_hybrid_retrieval(
            news_features=news_features,
            retrieval_k=effective_retrieval_limit,
            segment_filter=segment_filter,
            client_ids=None,
        )
        fallback_knn_hits = fallback_knn_response["hits"]["hits"]
        fallback_bm25_hits = fallback_bm25_response["hits"]["hits"]

    knn_hits = _dedupe_hits_by_client(knn_response["hits"]["hits"] + fallback_knn_hits)
    bm25_hits = _dedupe_hits_by_client(bm25_response["hits"]["hits"] + fallback_bm25_hits)

    rrf_k = 60
    rrf_scores: dict[str, float] = defaultdict(float)
    hit_sources: dict[str, dict] = {}
    hit_presence: dict[str, set[str]] = defaultdict(set)

    for rank, hit in enumerate(knn_hits, start=1):
        client_id = hit["_source"]["client_id"]
        rrf_scores[client_id] += 1 / (rrf_k + rank)
        hit_sources[client_id] = hit["_source"]
        hit_presence[client_id].add("knn")

    for rank, hit in enumerate(bm25_hits, start=1):
        client_id = hit["_source"]["client_id"]
        rrf_scores[client_id] += 1 / (rrf_k + rank)
        hit_sources.setdefault(client_id, hit["_source"])
        hit_presence[client_id].add("bm25")

    max_rrf = max(rrf_scores.values(), default=1.0)
    kept_results = []
    for client_id, raw_score in sorted(rrf_scores.items(), key=lambda item: -item[1]):
        source = hit_sources[client_id]
        signal = signals_by_client.get(client_id) or _build_prefilter_signal(
            source,
            news_features,
        )
        normalized_score = round(raw_score / max_rrf, 4)
        has_structured_signal = any(
            [
                signal["has_direct_ticker_match"],
                signal["has_tag_overlap"],
                signal["has_classification_overlap"],
                signal["has_mandate_fit"],
            ]
        )
        semantic_only = not has_structured_signal
        keep_candidate = False

        if signal["has_direct_ticker_match"]:
            keep_candidate = True
        elif has_structured_signal and normalized_score >= structured_min_score:
            keep_candidate = True
        elif (
            (broad_macro or not prefiltered_ids)
            and semantic_only
            and hit_presence[client_id] == {"knn", "bm25"}
            and normalized_score >= semantic_only_min_score
        ):
            keep_candidate = True

        if not keep_candidate:
            continue

        kept_results.append(
            {
                "client_id": client_id,
                "client_name": source["client_name"],
                "relevance_score": normalized_score,
                "has_direct_ticker_match": signal["has_direct_ticker_match"],
                "has_tag_overlap": signal["has_tag_overlap"],
                "has_classification_overlap": signal["has_classification_overlap"],
                "has_mandate_fit": signal["has_mandate_fit"],
                "ticker_overlap_count": signal["ticker_overlap_count"],
                "tag_overlap_count": signal["tag_overlap_count"],
                "classification_overlap_count": signal["classification_overlap_count"],
                "matched_tickers": signal["matched_tickers"],
                "matched_isins": signal["matched_tickers"],
                "matched_tags": signal["matched_tags"],
                "matched_classifications": signal["matched_classifications"],
                "selection_reason": _build_selection_reason(
                    signal,
                    normalized_score,
                    semantic_only,
                ),
                "classification_weights": source.get("classification_weights", {}),
                "client_portfolio_document": source,
            }
        )

    final_cap = final_limit
    if "hnw" in {str(segment).strip().lower() for segment in client_segments or []}:
        default_hnw_cap = max(int(settings.HNW_RELEVANCE_FINAL_TOP_N), 1)
        broad_hnw_cap = max(int(settings.HNW_RELEVANCE_BROAD_TOP_N), default_hnw_cap)
        final_cap = min(final_cap, broad_hnw_cap if broad_macro else default_hnw_cap)

    results = sorted(
        kept_results,
        key=lambda item: (
            not item["has_direct_ticker_match"],
            not item["has_tag_overlap"],
            not item["has_classification_overlap"],
            -item["ticker_overlap_count"],
            -item["tag_overlap_count"],
            -item["classification_overlap_count"],
            -item["relevance_score"],
        ),
    )[:final_cap]

    print(
        "[Relevance] "
        f"news_id={news_doc.get('id', news_doc.get('title', 'unknown'))} "
        f"segments={client_segments or ['all']} "
        f"broad_macro={broad_macro} "
        f"clients_before={len(client_docs)} "
        f"prefilter_after={len(prefiltered_ids)} "
        f"hybrid_candidates={len(rrf_scores)} "
        f"threshold_survivors={len(kept_results)} "
        f"final_selected={len(results)}"
    )
    for selected in results:
        print(
            "[Relevance] "
            f"selected_client={selected['client_id']} "
            f"score={selected['relevance_score']} "
            f"reason={selected['selection_reason']}"
        )

    return results


def process_news_stream(
    news_docs: list[dict],
    top_k: int | None = None,
    min_score: float | None = None,
    client_segments: list[str] | None = None,
    retrieval_k: int | None = None,
    final_top_n: int | None = None,
) -> dict[str, list[dict]]:
    results = {}
    for doc in news_docs:
        news_id = doc.get("id", doc.get("title", "unknown"))
        matched_clients = score_news_against_clients(
            doc,
            top_k=top_k,
            min_score=min_score,
            client_segments=client_segments,
            retrieval_k=retrieval_k,
            final_top_n=final_top_n,
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
