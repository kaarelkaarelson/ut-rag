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

    if not os.path.exists("docs"):
        os.makedirs("docs")

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
                        folder_path = "docs/"
                        creation_path = os.path.join(folder_path, domain)
                        os.mkdir(creation_path)
                    i += 1

                    with open(f'docs/{domain}/{file_name}', 'w', encoding='utf-8') as file:
                        file.write('<LINK>{}</LINK>'.format(link) + '\n' 
                                   + preprocessed_html)
                except Exception as e:
                    print(f"Failed to download {link}: {e}")


def remove_unneeded(links_folder):
    for folder in links_folder:
        list_of_txt = os.listdir(f"./Texts/{folder}")
        for file in list_of_txt:
            if "panopto" in file or "moodle" in file or "ois2" in file:
                print(f"Deleted {file}")
                os.remove(f"./Texts/{folder}/{file}")

FORBIDDEN_SUBDOMAINS = []

with open('forbidden_subdomains.txt', 'r', ) as f:
    FORBIDDEN_SUBDOMAINS = [line.strip() for line in f.readlines()]

def remove_unneeded_links(folder_paths):
    
    for folder_path in folder_paths:
        links_new = []
        links = []
        removed_links = []

        file_path = f"{folder_path}/links.txt" 

        with open(file_path, "r", newline='') as f:
            for line in f:
                links.append(line.rstrip('\n'))

        print(links)

        for link in links: 
            if any(subdomain in link for subdomain in FORBIDDEN_SUBDOMAINS):
                print(f"DELETED: {link}")
                removed_links.append(link)
                continue
            else:
                links_new.append(link)
            
        print(f"LINKS OLD: {links} \n")
        print(f"LINKS NEW: {links_new} \n")

        print(f"REMOVED LINKS: {removed_links} \n")


        with open(file_path, 'w') as f:
            for link in links_new:
                f.write(link)

        with open(f"{folder_path}/removed_links.txt", 'w') as f:
            for link in removed_links:
                f.write(link)
