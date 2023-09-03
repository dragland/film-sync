import requests
import concurrent.futures
from bs4 import BeautifulSoup


session = requests.Session()


def scrape_info(url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    film = soup.find(class_='film-header-lockup -default')
    title = film.find('h1', class_='headline-1').get_text(strip=True)
    try:
        year = film.find('small', class_='number').find('a').get_text(strip=True)
    except AttributeError:
        year = None
    return title, year


def scrape_urls(base, page):
    response = session.get(f"{base}/page/{page}/")
    soup = BeautifulSoup(response.text, 'html.parser')

    posters = soup.find_all(class_='poster-container')
    page_urls = [f"https://letterboxd.com{poster.find('div')['data-target-link']}" for poster in posters]
    return page_urls


def get_watchlist(url):
    print("Reading letterboxd watchlist...")
    urls = []
    page = 1
    while True:
        print(page)
        page_urls = scrape_urls(url, page)
        if not page_urls:
            break
        urls.extend(page_urls)
        page += 1

    print("Extracking film titles & years...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        films = set(executor.map(scrape_info, urls))
    return films