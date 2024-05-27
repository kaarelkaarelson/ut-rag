import os
import subprocess

def run_scrapy_crawl():
    command = "python -m streamlit run ./app.py"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    run_scrapy_crawl()
