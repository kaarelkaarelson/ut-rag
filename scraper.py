import requests as req
from bs4 import BeautifulSoup as bs
import os
import re
from utils.url import normalize_url

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

def download_pages(domains):
    for domain in domains:
        with open("links/" + domain + "/links.txt", "r") as f:
            links = [line.strip() for line in f.readlines()]
            i = 0
            for link in links:
                try:
                    response = req.get(link)
                    html = response.text
                    preprocessed_html = extract_text_content(html) # Choose if you extract_text_content() or remove_tags()

                    sanitized_link = sanitize_link(link).replace(".", "_")
                    file_name = sanitized_link + '.txt'

                    if i == 0: #Stupid solution but works
                        folder_path = "Texts/"
                        creation_path = os.path.join(folder_path, domain)
                        os.mkdir(creation_path)
                    i += 1

                    with open(f'Texts/{domain}/{file_name}', 'w', encoding='utf-8') as file:
                        file.write(preprocessed_html)
                except Exception as e:
                    print(f"Failed to download {link}: {e}")

if __name__ == '__main__':
    dir_as_list = os.listdir("./links")
    download_pages(dir_as_list)