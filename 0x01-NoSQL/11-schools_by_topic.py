#!/usr/bin/env python3
"""
Contains a function that lists
school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """lists schools having a specific topic"""
    return mongo_collection.find({"topics": topic})
