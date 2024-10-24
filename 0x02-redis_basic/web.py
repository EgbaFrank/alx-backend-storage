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
        key = f"count:{args[0]}"
        _redis.setnx(key, 0)
        _redis.expire(key, 10)
        _redis.incr(key)

        return func(*args)
    return wrapper


@count_access
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    response = requests.get(url)

    return response.text
