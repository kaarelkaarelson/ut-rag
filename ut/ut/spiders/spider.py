import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

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
        links = response.css("a::attr(href)").getall()

        with open('ut_links.txt', 'a') as file:
            file.write(response.url + '\n')

        for link in links:
            if link is not None and ("ut.ee" in link or link.startswith('/')) and not link.startswith("mailto:"):
                # print(link)
                link = response.urljoin(link)
                yield scrapy.Request(link, callback=self.parse)

