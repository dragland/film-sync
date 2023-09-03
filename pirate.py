#!/usr/bin/env python3


import argparse
import requests


def search_tpb(query):
    base_url = "https://apibay.org/q.php"
    params = {
        "q": query,
        "cat": "all",
        "orderby": "seeds",
        "format": "json",
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error querying TPB API:", response.status_code)