# News To Insight Workflow

This is the main end-to-end business path in the current Docker runtime.

## Sequence

```mermaid
sequenceDiagram
    participant NP as news_provider
    participant EH as eventhub
    participant DPSN as dps_news_processor
    participant COS as cosmos-emulator
    participant FUNC as functions
    participant SB as servicebus-emulator
    participant MAS as mas
    participant MDB as Mongo backup/read store
    participant UIAPI as ui-api
    participant UI as ui

    NP->>EH: publish enriched Benzinga payload
    EH->>DPSN: deliver Event Hub message
    DPSN->>COS: upsert normalized news doc
    DPSN->>MDB: mirror news doc when backup enabled
    COS->>FUNC: Cosmos DB trigger fires
    FUNC->>SB: enqueue realtime-news-events
    FUNC->>SB: schedule delayed-news-events
    SB->>MAS: deliver HNW and standard workflow jobs
    MAS->>COS: read news, client profiles, holdings
    MAS->>SB: enqueue generate-insight-events
    SB->>MAS: deliver generate insight job
    MAS->>COS: write insight + monitoring updates
    MAS->>MDB: mirror insight/read updates when backup enabled
    UI->>UIAPI: GET /api/*
    UIAPI->>MDB: query Mongo collections
```

## Phase Breakdown

### 1. Ingestion

- `news_provider` polls Benzinga once per minute.
- It keeps a rolling `updatedSince` cursor with a one-minute overlap to reduce missed updates.
- Each raw article is enriched with ingestion metadata before being sent to Event Hub.

### 2. Normalization And Persistence

- `dps_news_processor` consumes the Event Hub stream using consumer group `DPS`.
- It normalizes article fields into a stable document shape.
- It stamps the document with:
  - `dps_news_processor=stored`
  - `retail_batch=pending`
- It upserts the result into Cosmos and checkpoints the Event Hub message.

### 3. Queue Dispatch

- `functions.change_feed_service` reacts to new Cosmos documents and publishes `realtime_news` messages to `realtime-news-events`.
- It skips documents already marked with `monitoring.stages.change_feed_to_mas`.
- `functions.standard_trigger` periodically schedules `standard_news` messages onto `delayed-news-events`.

### 4. Workflow Routing In MAS

- realtime queue -> `hnw` workflow
- delayed queue -> `standard` workflow
- generate insight queue -> `generate_insight` workflow

Both HNW and standard workflows:

- retrieve candidate clients through Elasticsearch-backed relevance search
- ground those candidates against holdings snapshots in Cosmos
- assign an execution route:
  - `full_loop`
  - `single_pass_indirect`
  - `skip`
- publish per-client insight jobs when the candidate survives routing

### 5. Insight Generation

- `generate_insight` builds a compact portfolio context.
- It generates an insight draft with the LLM backend.
- Full-loop jobs pass through precheck plus verifier scoring.
- Single-pass indirect jobs skip verifier and persist immediately.
- Final results are written into the insights container and optionally mirrored to Mongo.

## Route Split

```mermaid
flowchart TD
    N[Normalized news doc] --> CF[Change feed queues realtime job]
    N --> RB[Retail batch marked pending]
    RB --> ST[Timer schedules delayed job]
    CF --> HNW[MAS HNW workflow]
    ST --> STD[MAS standard workflow]
    HNW --> GI[generate_insight job]
    STD --> GI
    GI --> SAVE[Insight persisted]
```

## What The UI Sees

- The React UI does not call Cosmos directly.
- `ui-api` exposes read-only endpoints over Mongo-backed collections.
- Ops pages show monitoring stage history derived from the mirrored news documents.
- Client pages show client profiles and saved insights from the mirrored collections.
