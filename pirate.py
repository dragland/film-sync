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


def _size_hr(size, decimals=2):
    size = float(size)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimals}f}{unit}"


def _magnet_link(info_hash):
    base_magnet_link = "magnet:?xt=urn:btih:"
    return base_magnet_link + info_hash