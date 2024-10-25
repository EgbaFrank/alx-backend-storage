#!/usr/bin/env python3
"""
Provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()

    logs = client.logs.nginx

    total_logs = logs.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    method_counts = {}
        
    # Initialize counts for each method to 0
    for method in methods:
        method_counts[method] = logs.count_documents({"method": method})

    get_status_count = logs.count_documents({"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")  # First line: total number of logs
    print("Methods:")  # Second line: header for methods
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")  # Count for each method

    # Line for GET requests to /status
    print(f"{get_status_count} status check")
