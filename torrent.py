import requests


def add_magnet_link(url, username, password, magnet):
    auth_response = requests.post(
        f"{url}/api/v2/auth/login",
        data={"username": username, "password": password}
    )
    auth_cookie = auth_response.cookies.get("SID")

    add_response = requests.post(
        f"{url}/api/v2/torrents/add",
        headers={"Cookie": f"SID={auth_cookie}"},
        data={"urls": magnet}
    )
    if add_response.status_code == 200:
        print(f"{url}: Succesfully queued {magnet}")
    else:
        print(f"Error queing {magnet}:", add_response.text)