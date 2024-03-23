import requests as req
from bs4 import BeautifulSoup as bs
import os
import re

def normalize_url(url):
    if "https://www." in url:
        return url.replace("https://www.", "https://")
    return url

def get_links_from_page(url):
    r = req.get(url)
    soup = bs(r.text, 'html.parser')
    tags = soup.find_all('a')

    links = [normalize_url(url)] 
    for tag in tags:
        href = tag.get('href')
        if href:
            normalized_href = normalize_url(href)
            if "ut.ee" in normalized_href and not normalized_href.startswith("mailto:") and normalized_href not in links:
                links.append(normalized_href) 

    return links 

def sanitize_filename(url):
    """
    Sanitizes the URL to be used as a valid filename by removing or replacing invalid characters.
    """
    # Remove the scheme (http, https) and replace invalid characters with underscores
    sanitized = re.sub(r'https?://', '', url)  # Remove scheme
    sanitized = re.sub(r'[^a-zA-Z0-9\-_\.]', '_', sanitized)  # Replace invalid chars with underscore
    return sanitized

def download_pages(links):
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    for link in links:
        try:
            response = req.get(link)
            sanitized_link = sanitize_filename(link)
            file_name = sanitized_link + '.html'
            with open(f'docs/{file_name}', 'w', encoding='utf-8') as file:
                file.write(response.text)
        except Exception as e:
            print(f"Failed to download {link}: {e}")

links = get_links_from_page('https://www.ut.ee')
download_pages(links)
print(links)

