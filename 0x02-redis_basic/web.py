#!/usr/bin/env python3
"""
Implements a get_page function
"""
import requests
import redis
from typing import Callable
import functools


def count_access(func: Callable) -> Callable:
    """
    Track how many times a particular URL was accessed
    """
    @functools.wraps(func)
    def wrapper(*args):
        _redis = redis.Redis()

        url = args[0] if args else "unknown"

        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        _redis.setnx(count_key, 0)
        _redis.incr(count_key)

        cached_page = _redis.get(cache_key)
        if cached_page:
            return cached_page.decode("utf-8")

        result = func(*args)
        _redis.setex(cache_key, 10, result)

        return result
    return wrapper


@count_access
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    response = requests.get(url)

    return response.text
