import os
from src.scraper import remove_unneeded_links


if __name__ == '__main__':
    dir_as_list = [f"./links/{folder}" for folder in os.listdir("./links")]
    print(dir_as_list)
    remove_unneeded_links(dir_as_list)
