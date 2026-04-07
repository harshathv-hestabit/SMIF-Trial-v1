# Documentation Hub

This directory splits SMIF documentation into four layers:

- Runtime: how `src/docker-compose.yaml` boots, wires, and gates services.
- Services: one README per Compose service, including separate infra READMEs.
- Workflows: cross-service business logic and end-to-end sequences.
- Storage and contracts: shared payload, queue, and persistence rules.

## Start Here

- [Docker Runtime](docker-runtime/README.md)
- [Storage and Contracts](storage-and-contracts/README.md)
- [News To Insight Workflow](workflows/news-to-insight/README.md)
- [Portfolio And Relevance Workflow](workflows/portfolio-and-relevance/README.md)

## Service READMEs

### Infrastructure

- [azurite](docker-services/azurite/README.md)
- [cosmos-emulator](docker-services/cosmos-emulator/README.md)
- [eventhub](docker-services/eventhub/README.md)
- [servicebus-emulator](docker-services/servicebus-emulator/README.md)
- [mssql](docker-services/mssql/README.md)
- [elasticsearch](docker-services/elasticsearch/README.md)

### Application

- [backup_copy](docker-services/backup_copy/README.md)
- [news_provider](docker-services/news_provider/README.md)
- [dps_news_processor](docker-services/dps_news_processor/README.md)
- [dps_client_processor](docker-services/dps_client_processor/README.md)
- [functions](docker-services/functions/README.md)
- [mas](docker-services/mas/README.md)
- [ui-api](docker-services/ui-api/README.md)
- [ui](docker-services/ui/README.md)

## Important Runtime Note

The current UI read path is Mongo-backed:

- pipeline services write primary operational data into Cosmos DB
- successful writes can also be mirrored into Mongo when `MONGO_BACKUP_ENABLED=true`
- `backup_copy` restores Mongo data back into Cosmos at startup
- `ui-api` reads Mongo collections directly, not Cosmos

That split is intentional in the current code and is documented in [Storage and Contracts](storage-and-contracts/README.md).
