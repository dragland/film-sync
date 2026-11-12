import requests


def get_library(url, api_key):
    print(f"Querying server @{url}...")
    response = requests.get(
        f"{url}/Items",
        headers={"Authorization": f'MediaBrowser Token="{api_key}"'},
        params={
            "IncludeItemTypes": "Movie",
            "Recursive": "true",
            "Fields": "ProductionYear",
        },
    )
    response.raise_for_status()

    library = set()
    for f in response.json()["Items"]:
        year = f.get("ProductionYear")
        library.add((f["Name"], str(year) if year else None))

    print(f"You have {len(library)} films in your library")
    return library
