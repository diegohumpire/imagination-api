import abc
from ..databases.redis_db import get_redis_connection

TTL_SECONDS = 15


class ICacheService(abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> str:
        pass

    @abc.abstractmethod
    def save(self, key: str, value: str):
        pass

    @abc.abstractmethod
    def exists(self, key: str) -> bool:
        pass


class RedisCacheService(ICacheService):
    redis = get_redis_connection()
    ttl = TTL_SECONDS

    def set_ttl(self, ttl: int):
        self.ttl = ttl
        return self

    def get(self, key: str) -> str:
        return self.redis.get(key)

    def save(self, key: str, value: str):
        self.redis.set(key, value, ex=self.ttl)

    def exists(self, key: str) -> bool:
        return self.redis.exists(key)
