# mas

`mas` is the orchestration and insight-generation service. It contains three distinct workflows inside one long-running process.

## Runtime Contract

- Compose service: `mas`
- Build file:
  - [src/app/modules/MAS/.dockerfile](../../../src/app/modules/MAS/.dockerfile)
- Entrypoint:
  - `python -m app.modules.MAS`
- Depends on:
  - `azurite`
  - `backup_copy`
  - `servicebus-emulator`
- Runtime dependencies not explicitly health-gated in Compose:
  - `cosmos-emulator`
  - `elasticsearch`
  - LLM backend configured through env

## Queue To Workflow Map

```mermaid
flowchart LR
    RT[realtime-news-events] --> HNW[hnw workflow]
    DL[delayed-news-events] --> STD[standard workflow]
    GI[generate-insight-events] --> GEN[generate_insight workflow]
```

## Message Handling Envelope

Before business logic runs, the service does message-level orchestration:

- receive one message at a time per worker semaphore
- decode JSON body
- validate the expected `event_type`
- run the mapped workflow
- `complete` on success
- `abandon` on failure below max delivery attempts
- `dead-letter` on failure at or above `SERVICEBUS_MAX_DELIVERY_ATTEMPTS`
- enable lock renewal for `generate_insight` messages

## HNW Workflow

```mermaid
flowchart TD
    E1[realtime_news message] --> F1[fetch news document from Cosmos]
    F1 --> S1[search client candidates in Elasticsearch]
    S1 --> C1[dedupe candidate clients]
    C1 --> G1[ground against holdings snapshot]
    G1 --> R1[assign execution route]
    R1 --> Q1[publish generate_insight jobs]
    Q1 --> M1[update monitoring stages]
```

Business intent:

- process newly arrived news quickly
- target the HNW client segment
- move only grounded candidates into generation

## Standard Workflow

```mermaid
flowchart TD
    E2[standard_news message] --> B2[query pending retail_batch news in Cosmos]
    B2 --> S2[search retail candidates in Elasticsearch]
    S2 --> G2[ground client/news pairs against holdings]
    G2 --> R2[assign execution route]
    R2 --> Q2[publish generate_insight jobs]
    Q2 --> M2[mark mas_standard completed and queue counts]
```

Business intent:

- process a time-windowed batch instead of one article at a time
- drain news documents previously marked `retail_batch=pending`
- update the source news documents with candidate and queue counts

## Generate Insight Workflow

```mermaid
flowchart TD
    START[generate_insight event] --> ROUTE{execution_route}
    ROUTE -->|skip| SKIP[mark skipped]
    ROUTE -->|full_loop| GEN[generate insight draft]
    ROUTE -->|single_pass_indirect| GEN2[generate insight draft]
    GEN --> PRE[precheck]
    PRE -->|pass| VER[verifier]
    PRE -->|fail and retries left| GEN
    PRE -->|fail and maxed out| FAIL[mark failed]
    VER -->|score >= 75| SAVE[save verified insight]
    VER -->|score < 75 and retries left| GEN
    VER -->|score < 75 and maxed out| FAIL
    GEN2 --> SAVE2[save single_pass_completed insight]
```

Execution routes:

- `full_loop`: generate, precheck, verify, then persist
- `single_pass_indirect`: generate once and persist without verifier
- `skip`: do not generate, record skipped outcome only

## Core Decisioning Inside MAS

### Retrieval

`mas` first retrieves candidate clients from Elasticsearch using:

- ticker overlap
- tag overlap
- classification overlap
- mandate/topic fit
- lexical relevance
- embedding similarity

### Grounding

It then grounds those candidates against holdings snapshots in Cosmos using:

- direct ISIN match
- direct ticker match
- direct underlying ticker match
- direct issuer match
- indirect currency overlap
- indirect macro-allocation overlap

### Route assignment

Route assignment decides whether the job deserves:

- full verifier loop
- indirect single pass
- skip

The main drivers are:

- grounded relevance
- direct match count
- matched symbol overlap
- holdings match count
- top holdings match score
- security-type alignment

## State Written By MAS

MAS writes to:

- news monitoring timeline and stage records in Cosmos
- insight documents in Cosmos
- mirrored Mongo collections when backup is enabled
- Service Bus `generate-insight-events`

## Why This Service Is The Most Important README

The `mas` container is where most of the business policy lives:

- client relevance thresholds
- HNW vs retail branching
- execution routing rules
- LLM generation and verifier loop
- retry and dead-letter behavior

If you need to understand why an insight was or was not produced, start here and then cross-reference the workflow docs.
