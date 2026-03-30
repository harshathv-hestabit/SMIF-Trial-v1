from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.aio import CosmosClient as AsyncCosmosClient


_COSMOS_CLIENT_OPTIONS = {
    "connection_verify": False,
    "enable_endpoint_discovery": False,
    "connection_timeout": 5,
}


def build_sync_cosmos_client(
    cosmos_url: str,
    cosmos_key: str,
) -> CosmosClient:
    return CosmosClient(
        cosmos_url,
        credential=cosmos_key,
        **_COSMOS_CLIENT_OPTIONS,
    )


def build_async_cosmos_client(
    cosmos_url: str,
    cosmos_key: str,
) -> AsyncCosmosClient:
    return AsyncCosmosClient(
        cosmos_url,
        credential=cosmos_key,
        **_COSMOS_CLIENT_OPTIONS,
    )


def get_database_client(
    client: CosmosClient | AsyncCosmosClient,
    database_name: str,
):
    return client.get_database_client(database_name)


def get_container_client(database_client, container_name: str):
    return database_client.get_container_client(container_name)


async def ensure_async_container(
    client: AsyncCosmosClient,
    *,
    database_name: str,
    container_name: str,
    partition_key_path: str,
):
    database = await client.create_database_if_not_exists(database_name)
    return await database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path=partition_key_path),
    )
