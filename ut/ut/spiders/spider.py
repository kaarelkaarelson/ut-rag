import scrapy
from urllib.parse import urlparse, parse_qs
import re

class LinkChecker:

    forbidden_query_params = ['add-to-cart', 
                              'algus%5Bvalue%5D%5Bdate%5D', 'liik', # utlib.ut.ee
                              ]
    forbidden_paths = ['/login.action']

    forbidden_subdomains = ['auth.ut.ee']

    def contains_forbidden_path(self, path):
        for forbidden_path in self.forbidden_paths:
            if forbidden_path in path:
                return True

    def contains_forbidden_subdomains(self, domain):
        for forbidden_subdomain in self.forbidden_subdomains:
            if forbidden_subdomain in domain:
                return True

    def contains_forbidden_query(self, query):
        query_params = parse_qs(query)

        if not query_params:
            if query: # check for no key-value pair query parameter
                print("NO KEY-VALUE PARAM: ", query_params)

                regex = "(http|https):\/\/.*"
                if re.match(regex, query):
                    return True
        else:
            print("PARAMS: ", query_params)
            for forbidden_query_param in self.forbidden_query_params:
                if forbidden_query_param in query_params.keys():
                    return True
            
            regex = "(http|https):\/\/.*"
            for key in query_params.keys():
                if re.match(regex, key):
                    return True


        return False

    def is_allowed_link(self, abs_link):
        if "mailto:" in abs_link or "tel:" in abs_link:
            return False
        
        parsed_url = urlparse(abs_link)
        netloc = parsed_url.netloc
        path = parsed_url.path
        query = parsed_url.query

        if not "ut.ee" in netloc:
            return False
        if self.contains_forbidden_subdomains(netloc):
            return False
        if self.contains_forbidden_path(path):
            return False
        if self.contains_forbidden_query(query): # if any of the forbidden query params are present
            return False

        return True

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    link_checker = LinkChecker()

    def start_requests(self):
        urls = [
            "https://ut.ee/et/avaleht"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def download_url(self):
        # url = response.url.split("/")[-2] 
        # filename = f"ut-{url}.html"
        # Path(filename).write_bytes(response.body)
        pass

    def parse(self, response):

        abs_link = response.url

        if not self.link_checker.is_allowed_link(abs_link): 
            with open('forbidden_links.txt', 'a') as file:
                file.write(response.url + '\n')
            return

        print("ALLOWED LINK: ", abs_link)
        with open('ut_links.txt', 'a') as file:
            file.write(response.url + '\n')

        links = response.css("a::attr(href)").getall()

        for link in links:

            if link is not None:
                abs_link = response.urljoin(link)

                # if self.link_checker.is_allowed_link(abs_link): 
                #     print("ALLOWED LINK: ", abs_link)
                #     yield scrapy.Request(abs_link, callback=self.parse)
                yield scrapy.Request(abs_link, callback=self.parse)

    

