#!/usr/bin/env python3
import configparser
from plex import get_library
from letterboxd import get_watchlist
from pirate import pick_torrent
from torrent import add_magnet_link


config = configparser.ConfigParser()
config.read('config.ini')


def main():
    library = get_library(config.get('URLS', 'plex_url'), config.get('API_KEYS', 'plex_token'))
    watchlist = get_watchlist(config.get('URLS', 'watchlist_url'))

    todo = watchlist - library
    print(f"You still are missing {len(todo)} films")
    for film in todo:

        magnet = pick_torrent(f"{film[0]} {film[1]} 1080p")
        if not magnet:
            magnet = pick_torrent(f"{film[0]} {film[1]}")
        if magnet and magnet != "n":
            add_magnet_link(config.get('URLS', 'qb_url'), config.get('API_KEYS', 'qb_username', config.get('API_KEYS'), 'qb_password'), magnet)


if __name__ == "__main__":
    main()