import scrapy
from urllib.parse import urlparse, parse_qs
import re

SUB_DOMAIN = "nlp.cs.ut.ee"

subdomains = []

with open('subdomains_clean.txt', 'r') as file:
    subdomains = ['https://' + link.strip() if not link.strip().startswith(('http://', 'https://')) else link.strip() for link in file.readlines()]


class QuotesSpider(scrapy.Spider):
    name = "subdomain_filter"

    def start_requests(self):
        urls = subdomains

        print(subdomains)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'dont_retry': True})

    def parse(self, response):
        abs_url = response.url
        print("URL exists: ", abs_url)

        with open("subdomains_active.txt", 'w') as file:
            file.write(abs_url + '\n')
            print("WROTE URL: ", abs_url)

    def errback(self, failure):
        pass
    


