
import requests as req
from bs4 import BeautifulSoup as bs

def get_links_from_page(url):
    r = req.get(url)
    soup = bs(r.text, 'html.parser')
    tags = soup.find_all('a')
    links = set(tag.get('href') for tag in tags if tag.get('href') is not None and "ut.ee" in tag.get('href') and not tag.get('href').startswith("mailto:"))

    return links 

links = get_links_from_page('https://www.ut.ee')

print(links)