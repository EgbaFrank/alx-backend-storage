#!/usr/bin/env python3
"""
Contains a mongodb insert function
"""


def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection"""
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)
