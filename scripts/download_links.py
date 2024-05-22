import os
from src.scraper import download_pages


if __name__ == '__main__':
    dir_as_list = os.listdir("./links")
    print(dir_as_list)
    # download_pages(dir_as_list)
    download_pages(["ut_ee"])
