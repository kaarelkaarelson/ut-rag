import scrapy
from urllib.parse import urlparse, parse_qs
import re

SUB_DOMAIN = "nlp.cs.ut.ee"
OUTPUT_FILE = "subdomains_active.txt"

subdomains = []

with open('subdomains_clean.txt', 'r') as file:
    subdomains = ['https://' + link.strip() if not link.strip().startswith(('http://', 'https://')) else link.strip() for link in file.readlines()]

# subdomains = ['https://ns.ut.ee', 'https://www.neuro.cs.ut.ee', 'https://tartumodelun.ut.ee', 'https://cybersecurity.cs.ut.ee', 'https://review-203.dev.gi.ut.ee']

with open(OUTPUT_FILE, 'w') as file:
    file.write("")
    print("OUTPUT FILE")

class QuotesSpider(scrapy.Spider):
    name = "subdomain_filter"

    def start_requests(self):
        urls = subdomains

        print(subdomains)

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
    


