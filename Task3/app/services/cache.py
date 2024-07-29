from redis import Redis
from app.core.config import settings

redis_client = Redis.from_url(settings.REDIS_URL)

def get_cached_data(key: str):
    return redis_client.get(key)

def set_cache_data(key: str, value: str, ttl: int = 3600):
    redis_client.set(key, value, ex=ttl)