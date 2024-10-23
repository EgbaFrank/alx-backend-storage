#!/usr/bin/env python3
"""
Contain a Cache Class
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any, Optional
import functools


def call_history(method: Callable) -> Callable:
    """
    Decorator function to track I/O operations
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inkey = f"{method.__qualname__}:inputs"
        outkey = f"{method.__qualname__}:outputs"
        self._redis.rpush(inkey, str(args))
        out = method(self, *args, **kwargs)
        self._redis.rpush(outkey, out)

        return out
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator function to track function calls
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.setnx(key, 0)
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper


def replay(func: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    _redis = redis.Redis()
    func_name = func.__qualname__
    ins = _redis.lrange(f"{func_name}:inputs", 0, -1)
    outs = _redis.lrange(f"{func_name}:outputs", 0, -1)
    call_count = _redis.get(func_name).decode('utf-8')
    print(f"{func_name} was called {call_count} times:")

    for arg, out in zip(ins, outs):
        arg = arg.decode("utf-8")
        out = out.decode("utf-8")
        print(f"{func_name}(*{arg}) -> {out}")


class Cache():
    """
    Definitions of a cache instance
    """
    def __init__(self):
        """initization function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
