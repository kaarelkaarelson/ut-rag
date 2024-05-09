import scrapy
from urllib.parse import urlparse, parse_qs
import re

# from utils.url import normalize_url

SUB_DOMAIN = "nlp.cs.ut.ee"
OUTPUT_FILE = "subdomains_active.txt"

subdomains = []

def normalize_url(url):
    url_norm = url.strip()
    
    if not url_norm.startswith(('http://', 'https://')):
        url_norm = 'https://' + url_norm
    if "https://www." in url_norm:
        return url_norm.replace("https://www.", "https://")
    elif "http://www." in url_norm:
        return url_norm.replace("http://www.", "http://")
    else: 
        return url_norm



with open('subdomains_clean.txt', 'r') as file:
    subdomains = [normalize_url(link) for link in file.readlines()]

def filter_second_level_subdomains(subdomains):
    second_level_subdomains = []
    for subdomain in subdomains[:3]:
        prefix = subdomain.split('ut.ee')[0].split("://")[1]
        print(prefix)

        parts = prefix.split('.')
        print(parts)
        if len(parts) == 1:
            second_level_subdomains.append(subdomain)  # Join the first two parts
    # return second_level_subdomains

subdomains = filter_second_level_subdomains(subdomains)

# subdomains = ['https://ns.ut.ee', 'https://www.neuro.cs.ut.ee', 'https://tartumodelun.ut.ee', 'https://cybersecurity.cs.ut.ee', 'https://review-203.dev.gi.ut.ee']

with open(OUTPUT_FILE, 'w') as file:
    file.write("")
    print("OUTPUT FILE")

class QuotesSpider(scrapy.Spider):
    name = "subdomain_filter"

    def start_requests(self):
        urls = subdomains

        print("SUBDOMAINS", subdomains)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'dont_retry': True}) # NB! set ROBOTSTXT_OBEY = False in settings.py

    def parse(self, response):
        abs_url = response.url
        print("URL exists: ", abs_url)

        with open(OUTPUT_FILE, 'a') as file:
            file.write(abs_url + '\n')
            print("WROTE URL: ", abs_url)

    def errback(self, failure):
        pass
    