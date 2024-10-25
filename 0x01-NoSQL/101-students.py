#!/usr/bin/env python3
"""
Contains a function that returns all students
sorted by average score
"""



def top_students(mongo_collection):
    """returns all students sorted by average score"""

    pipeline = [
            {
                "$unwind": "$topics"
            },
            {
                "$group": {
                    "_id": "$_id",
                    "name": {"$first": "$name"},
                    "averageScore": {"$avg": "$topics.score"}
                }
            },
            {
                "$sort": {"averageScore": -1}
            }
        ]

    return mongo_collection.aggregate(pipeline)
