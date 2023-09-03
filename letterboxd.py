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