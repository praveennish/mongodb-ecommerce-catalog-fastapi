from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import settings

_client: MongoClient = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        try:
            _client = MongoClient(
                settings.mongo_uri,
                uuidRepresentation='standard',
                minPoolSize=settings.mongo_min_pool_size,
                maxPoolSize=settings.mongo_max_pool_size,
                retryWrites=True
            )
        except ConnectionFailure as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {e}")
    return _client

def get_db() -> str:
    client = get_client()
    return client[settings.mongo_db]

def close_client():
    global _client
    if _client:
        _client.close()
        _client = None

def ping() -> bool:
    try:
        client = get_client()
        client.admin.command('ping')
        return True
    except ConnectionFailure:
        return False