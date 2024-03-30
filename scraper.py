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

def sanitize_link(url):
    """
    Sanitizes the URL to be used as a valid filename by removing the scheme (http, https) 
    and replaces invalid characters (like backslashes) with underscores
    """
    sanitized = re.sub(r'https?://', '', url) 
    sanitized = re.sub(r'[^a-zA-Z0-9\-_\.]', '_', sanitized) 
    return sanitized

def extract_text_content(html):
    """
    Removes all the html tags and keeps only text from the html page
    """
 
    soup = bs(html, "html.parser")
 
    for data in soup(['style', 'script']):
        data.decompose()
 
    return ' '.join(soup.stripped_strings)

def download_pages(links):
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    for link in links:
        try:
            response = req.get(link)
            html = response.text
            preprocessed_html = extract_text_content(html) # Choose if you extract_text_content() or remove_tags()

            sanitized_link = sanitize_link(link)
            file_name = sanitized_link + '.txt'
            with open(f'docs_unstructured/{file_name}', 'w', encoding='utf-8') as file:
                file.write(preprocessed_html)
        except Exception as e:
            print(f"Failed to download {link}: {e}")

if __name__ == '__main__':
    links = get_links_from_page('https://www.ut.ee')
    download_pages(links)
    print(links)