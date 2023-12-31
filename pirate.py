#!/usr/bin/env python3
import argparse
import configparser
import requests
from torrent import add_magnet_link


config = configparser.ConfigParser()
config.read('config.ini')


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
        print(f"{n}) ({_size_hr(t['size'])})\'{t['name']}\'[{t['username']}], Seeds:{t['seeders']}, Leeches:{t['leechers']}")
    try:
        selection = input("Enter the index of the torrent you want to use, or 'n' to skip: ")
        if selection == 'n':
            return "n"

        return _magnet_link(torrents[int(selection)]['info_hash'])
    except (ValueError, IndexError):
        print("Invalid index. Please enter a valid index.")


def download_torrent(query, download_flag=False):
    magnet = pick_torrent(query)
    if magnet and magnet != "n":
        if download_flag:
            add_magnet_link(
                config.get('URLS', 'qb_url'),
                config.get('API_KEYS', 'qb_username'),
                config.get('API_KEYS', 'qb_password'),
                magnet
            )
        else:
            print(f"Selected: {magnet}")
            print("Use the --download flag to queue this magnet link.")


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search The Pirate Bay from the command line")
    parser.add_argument("query", help="Search query (enclose in quotes if it contains spaces)")
    parser.add_argument("--download", action="store_true", help="Flag to add the queue torrent to your client")
    args = parser.parse_args()

    download_torrent(args.query, args.download)