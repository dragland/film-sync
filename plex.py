import requests
import xml.etree.ElementTree as ET


def get_library(url, token):
    print(f"Querying server @{url}...")
    plex_url = f"{url}/library/sections/2/all"
    response = requests.get(plex_url, headers={"X-Plex-Token": token})
    xml = ET.fromstring(response.text)

    library = set()
    for f in xml.iter('Video'):
        title = f.get('title')
        year = f.get('year')
        library.add((title, year))

    print(f"You have {len(library)} films in your library")
    return library