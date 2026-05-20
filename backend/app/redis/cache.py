import json
import logging
from collections.abc import Callable
from typing import Any

from app.redis.connection import redis_manager

logger = logging.getLogger(__name__)


async def cache_get(key: str) -> Any | None:
    client = redis_manager.client
    data = await client.get(key)
    if data is None:
        return None
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return data


async def cache_set(key: str, value: Any, ttl: int = 300) -> None:
    client = redis_manager.client
    serialized = json.dumps(value, default=str)
    await client.setex(key, ttl, serialized)


async def cache_delete(key: str) -> None:
    client = redis_manager.client
    await client.delete(key)


async def cache_delete_pattern(pattern: str) -> None:
    client = redis_manager.client
    cursor = 0
    while True:
        cursor, keys = await client.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            await client.delete(*keys)
        if cursor == 0:
            break


async def cache_or_fetch(key: str, ttl: int, fetcher: Callable[[], Any]) -> Any:
    cached = await cache_get(key)
    if cached is not None:
        return cached
    value = await fetcher()
    await cache_set(key, value, ttl)
    return value
