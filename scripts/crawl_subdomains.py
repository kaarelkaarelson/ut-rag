import os
import subprocess

def run_scrapy_crawl():
    command = "scrapy crawl subdomains"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    run_scrapy_crawl()
