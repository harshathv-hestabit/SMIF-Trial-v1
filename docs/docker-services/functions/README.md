# functions

`functions` is the Azure Functions host that converts stored news into workflow queue activity.

## Runtime Contract

- Compose service: `functions`
- Build file:
  - [src/app/functions/.dockerfile](../../../src/app/functions/.dockerfile)
- HTTP port:
  - `7071`
- Depends on:
  - `azurite`
  - `backup_copy`
  - `servicebus-emulator`
- Startup wrapper:
  - [src/app/functions/start.sh](../../../src/app/functions/start.sh)

## Host Boot Flow

```mermaid
flowchart TD
    START[start.sh] --> CERT[download Cosmos emulator cert]
    CERT --> TRUST[update-ca-certificates]
    TRUST --> HOST[start Azure Functions host]
    HOST --> CFT[change_feed_service active]
    HOST --> TIMER[standard_trigger active]
```

The certificate bootstrap is necessary because the Functions image connects to the Cosmos emulator over HTTPS.

## Function 1: `change_feed_service`

### Binding

- trigger type: `cosmosDBTrigger`
- source container: configured `NEWS_CONTAINER`
- lease container: configured `CHANGE_FEED_LEASE_CONTAINER`

### Logic

```mermaid
sequenceDiagram
    participant COS as cosmos-emulator
    participant FUNC as change_feed_service
    participant SB as servicebus-emulator

    COS->>FUNC: changed news documents
    FUNC->>FUNC: skip docs already marked change_feed_to_mas
    FUNC->>SB: publish realtime_news message
    FUNC->>COS: record monitoring stage change_feed_to_mas=queued
```

Key behaviors:

- extracts `id` from each changed document
- ignores documents already marked in `monitoring.stages.change_feed_to_mas`
- publishes to `QUEUE_REALTIME_NEWS`
- records a monitoring update back on the source news document

## Function 2: `standard_trigger`

### Binding

- trigger type: `timerTrigger`
- schedule source: `STANDARD_TRIGGER_SCHEDULE`

### Logic

```mermaid
sequenceDiagram
    participant TIMER as standard_trigger
    participant SB as servicebus-emulator

    TIMER->>TIMER: compute now and enqueue_at
    TIMER->>TIMER: build job_id and payload
    TIMER->>SB: send standard_news with scheduled_enqueue_time_utc
```

Key behaviors:

- reads `STANDARD_TRIGGER_DELAY_MINUTES`
- validates delay is a non-negative integer
- publishes to `QUEUE_DELAYED_NEWS`
- uses Service Bus scheduled enqueue time instead of sleeping locally

## Why This Service Exists

It is the orchestration seam between data persistence and workflow execution:

- Cosmos change feed -> HNW path
- timer schedule -> retail batch path

The older DPS change-feed listener code still exists in the repo, but the Compose runtime uses Azure Functions as the active change-feed dispatcher.
