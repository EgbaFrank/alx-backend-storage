#!/usr/bin/env python3
"""
Contains a function to changes
all topics of a school document
"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
