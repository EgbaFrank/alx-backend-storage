#!/usr/bin/env python3
"""
Contain a Cache Class
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any, Optional


class Cache():
    """
    Definitions of a cache instance
    """
    def __init__(self):
        """initization function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in Redis
        """
        key = str(uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        convert the stored data back to the desired format
        If fn is not provided, return the raw Redis value.
        """
        data = self._redis.get(key)
        if not data:
            return None

        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """
        convert the stored data back to a string
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        convert the stored data back to an integer
        """
        return self.get(key, int)
