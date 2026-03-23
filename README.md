# SMIF

SMIF is an event-driven market insight system with three active runtime pieces:

- `DPS` ingests and transforms market news, stores it in Cosmos DB, and emits Event Hub events.
- `dispatch_realtime_eventhub_to_servicebus` is an Azure Functions bridge that reads Event Hub batches and republishes them to Service Bus queues.
- `MAS` consumes Service Bus events, matches news against client portfolios, generates insights, verifies them, and stores the results.

The local development stack uses Azure emulators plus Elasticsearch through Docker Compose.

## Architecture

```text
DPS
  -> Cosmos DB news container
  -> Event Hub: news-processed
  -> Azure Function: dispatch_realtime_eventhub_to_servicebus
  -> Service Bus queues
     - realtime-news-events
     - standard-news-events
     - generate-insight-events
  -> MAS workers
  -> Cosmos DB insights container
```

Event routing is based on `event_type`:

- `realtime_news` -> `QUEUE_REALTIME_NEWS`
- `standard_news` -> `QUEUE_STANDARD_NEWS`
- `generate_insight` -> `QUEUE_GENERATE_INSIGHT`

The queue topology for the Service Bus emulator is defined in [src/app/common/servicebus-config.json](/home/harshathvenkastesh/Desktop/SMIF/src/app/common/servicebus-config.json).

## Repository Layout

```text
README.md
src/
  docker-compose.yaml
  requirements.txt
  host.json
  local.settings.json.example
  dispatch_realtime_eventhub_to_servicebus/
    __init__.py
    function.json
  app/
    common/
      eventhub-config.json
      servicebus-config.json
      service_bus.py
    modules/
      DPS/
      MAS/
```

## Components

### DPS

Relevant files:

- [src/app/modules/DPS/streamlit_app.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/DPS/streamlit_app.py)
- [src/app/modules/DPS/pipeline.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/DPS/pipeline.py)
- [src/app/modules/DPS/services/change_feed_service.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/DPS/services/change_feed_service.py)
- [src/app/modules/DPS/services/standard_event_service.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/DPS/services/standard_event_service.py)

Current role:

- Accepts raw news input through the Streamlit UI.
- Transforms input documents into the internal news schema.
- Writes processed news into Cosmos DB.
- Publishes downstream events for the rest of the pipeline.

### Event Hub -> Service Bus bridge

Relevant files:

- [src/dispatch_realtime_eventhub_to_servicebus/__init__.py](/home/harshathvenkastesh/Desktop/SMIF/src/dispatch_realtime_eventhub_to_servicebus/__init__.py)
- [src/dispatch_realtime_eventhub_to_servicebus/function.json](/home/harshathvenkastesh/Desktop/SMIF/src/dispatch_realtime_eventhub_to_servicebus/function.json)
- [src/app/common/service_bus.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/common/service_bus.py)
- [src/local.settings.json.example](/home/harshathvenkastesh/Desktop/SMIF/src/local.settings.json.example)

Current role:

- Runs as a Python Azure Function with an `eventHubTrigger`.
- Reads batched events from `%EVENTHUB_NAME%`.
- Maps each event by `event_type` to a Service Bus queue.
- Rebuilds the payload with transport metadata such as `created_at`, `source`, and `queue_name`.
- Publishes with a small retry loop before surfacing a failure.

### MAS

Relevant files:

- [src/app/modules/MAS/__main__.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/__main__.py)
- [src/app/modules/MAS/workflow/hnw.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/workflow/hnw.py)
- [src/app/modules/MAS/workflow/standard.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/workflow/standard.py)
- [src/app/modules/MAS/workflow/generate_insight.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/workflow/generate_insight.py)
- [src/app/modules/MAS/ui/main.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/modules/MAS/ui/main.py)

Current role:

- Builds and indexes client portfolio data.
- Consumes Service Bus queue messages for realtime, standard, and insight-generation workflows.
- Matches relevant news to client portfolios.
- Generates and verifies insight documents.
- Stores client insights in Cosmos DB and exposes them through the Streamlit UI.

## Local Infrastructure

[src/docker-compose.yaml](/home/harshathvenkastesh/Desktop/SMIF/src/docker-compose.yaml) starts:

- `azurite` for Azure Storage and checkpointing
- `cosmos` for the Cosmos DB emulator
- `eventhub` for the Event Hubs emulator
- `servicebus-emulator` plus `mssql` for Service Bus queues
- `elasticsearch` for search and client matching
- `dps` for the DPS app and UI
- `mas` for the MAS workers and UI

Default local ports:

- DPS UI: `http://localhost:8501`
- MAS UI: `http://localhost:8502`
- Elasticsearch: `http://localhost:9200`
- Cosmos emulator: `https://localhost:8081`
- Azurite Blob: `http://127.0.0.1:10000`
- Event Hubs AMQP: `127.0.0.1:5672`
- Service Bus AMQP: `127.0.0.2:5672`
- Service Bus management API: `http://127.0.0.2:5300`

## Run With Docker

Work from [src](/home/harshathvenkastesh/Desktop/SMIF/src):

```bash
docker compose up --build
```

To stop and remove persisted local emulator data:

```bash
docker compose down -v
```

## Run Locally

Create a virtual environment and install dependencies from [src/requirements.txt](/home/harshathvenkastesh/Desktop/SMIF/src/requirements.txt):

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1. Start local infrastructure

```bash
docker compose up azurite cosmos eventhub servicebus-emulator mssql elasticsearch
```

### 2. Configure local settings

Copy [src/local.settings.json.example](/home/harshathvenkastesh/Desktop/SMIF/src/local.settings.json.example) to `src/local.settings.json` and update values if your local setup differs.

For the Azure Functions bridge, the required settings are:

- `AzureWebJobsStorage`
- `FUNCTIONS_WORKER_RUNTIME`
- `EVENTHUB_NAME`
- `EVENTHUB_CONNECTION_STRING`
- `EVENTHUB_CONSUMER_GROUP`
- `SERVICEBUS_CONNECTION_STRING`
- `QUEUE_REALTIME_NEWS`
- `QUEUE_STANDARD_NEWS`
- `QUEUE_GENERATE_INSIGHT`

For DPS and MAS application settings, use [src/.env.example](/home/harshathvenkastesh/Desktop/SMIF/src/.env.example) as the baseline.

### 3. Start the bridge function

From `src/`, run the Azure Functions host:

```bash
func start
```

This loads [src/host.json](/home/harshathvenkastesh/Desktop/SMIF/src/host.json) and the function under [src/dispatch_realtime_eventhub_to_servicebus](/home/harshathvenkastesh/Desktop/SMIF/src/dispatch_realtime_eventhub_to_servicebus).

### 4. Start DPS and MAS

Run DPS:

```bash
streamlit run app/modules/DPS/streamlit_app.py
```

Run MAS workers:

```bash
python -m app.modules.MAS
```

Run the MAS UI separately if needed:

```bash
streamlit run app/modules/MAS/ui/main.py --server.port 8502
```

## Configuration

### Shared transport settings

The shared transport helpers live in [src/app/common/service_bus.py](/home/harshathvenkastesh/Desktop/SMIF/src/app/common/service_bus.py).

The emulator topologies live in:

- [src/app/common/eventhub-config.json](/home/harshathvenkastesh/Desktop/SMIF/src/app/common/eventhub-config.json)
- [src/app/common/servicebus-config.json](/home/harshathvenkastesh/Desktop/SMIF/src/app/common/servicebus-config.json)

### Application environment variables

[src/.env.example](/home/harshathvenkastesh/Desktop/SMIF/src/.env.example) currently includes:

- Cosmos DB settings
- Event Hub settings
- Service Bus settings
- Queue names and workflow concurrency controls
- Azure Storage checkpoint settings
- Elasticsearch URL
- LLM/API credentials such as `GROQ_API_KEY`, `GOOGLE_API_KEY`, `EODHD_API_KEY`, and `HF_TOKEN`

## Notes

- `local.settings.json` is for the Azure Functions host.
- `.env` or `.env.docker` is for DPS and MAS application configuration.
- The Service Bus emulator requires SQL Server; both are wired together in Docker Compose.
- The bridge currently supports `realtime_news`, `standard_news`, and `generate_insight` events only.
