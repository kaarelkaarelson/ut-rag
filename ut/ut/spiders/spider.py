import scrapy
from urllib.parse import urlparse, parse_qs
import re

SUB_DOMAIN = "nlp.cs.ut.ee"

class LinkChecker:

    subdomain = SUB_DOMAIN 

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
            # print("PARAMS: ", query_params)
            for forbidden_query_param in self.forbidden_query_params:
                if forbidden_query_param in query_params.keys():
                    return True
            
            regex = "(http|https):\/\/.*"
            for key in query_params.keys():
                if re.match(regex, key):
                    return True

        return False

class SubDomainUrlChecker:

    subdomain = SUB_DOMAIN

    allowed_links_file_name = subdomain.replace('.', '_') + '_links.txt' 
    forbidden_links_file_name = subdomain.replace('.', '_') + '_forbidden_links.txt' 

    forbidden_query_params = []
    forbidden_paths = []
    forbidden_subdomains = []

    def is_allowed_url(self, abs_url):
        if "mailto:" in abs_url or "tel:" in abs_url:
            return False
        
        parsed_url = urlparse(abs_url)
        netloc = parsed_url.netloc
        path = parsed_url.path
        query = parsed_url.query

        if not self.subdomain == netloc:
            print("NETLOC:", netloc)
            return False
        if self.contains_forbidden_subdomains(netloc):
            return False
        if self.contains_forbidden_path(path):
            return False
        if self.contains_forbidden_query(query): # if any of the forbidden query params are present
            return False

        return True

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
    
    def getAllowedLinksFileName(self):
        return self.allowed_links_file_name

    def getForbiddenLinksFileName(self):
        return self.allowed_links_file_name

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    url_checker = SubDomainUrlChecker()

    def start_requests(self):
        urls = [
            "https://nlp.cs.ut.ee/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def download_url(self):
        # url = response.url.split("/")[-2] 
        # filename = f"ut-{url}.html"
        # Path(filename).write_bytes(response.body)
        pass

    def parse(self, response):

        abs_url = response.url

        print("ALLOWED LINK: ", abs_url)
        with open(self.url_checker.allowed_links_file_name, 'a') as file:
            file.write(abs_url + '\n')

        links = response.css("a::attr(href)").getall()

        for link in links:
            if link is not None:
                abs_url = response.urljoin(link)

            if not self.url_checker.is_allowed_url(abs_url): 
                print("FORBIDDEN LINK: ", abs_url)

                with open(self.url_checker.forbidden_links_file_name, 'a') as file:
                    file.write(abs_url + '\n')
                continue     

            yield scrapy.Request(abs_url, callback=self.parse)

    

