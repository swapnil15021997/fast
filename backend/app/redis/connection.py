import logging

import redis.asyncio as aioredis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisManager:
    def __init__(self) -> None:
        self._client: aioredis.Redis | None = None

    async def connect(self) -> aioredis.Redis:
        if self._client is None:
            self._client = aioredis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password or None,
                decode_responses=True,
            )
            await self._client.ping()
            logger.info("Connected to Redis at %s:%s", settings.redis_host, settings.redis_port)
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.info("Redis connection closed")

    @property
    def client(self) -> aioredis.Redis:
        if self._client is None:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._client


redis_manager = RedisManager()
