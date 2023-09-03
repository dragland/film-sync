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


def pick_torrent(query):
    torrents = search_tpb(query)
    if torrents[0]['name'] == 'No results returned':
        print("No torrents found :(")
        return

    for n, t in enumerate(torrents):
        print(f"{n}) ({_size_hr(t['size'])})\'{t['name']}\'[{t['username']}], Seeds:{t['seeders']}, Leeches:{t['leechers']}: {_magnet_link(t['info_hash'])}")
    try:
        i = int(input("Enter the index of the torrent you want to use: "))
        return _magnet_link(torrents[i]['info_hash'])
    except (ValueError, IndexError):
        print("Invalid index. Please enter a valid index.")


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