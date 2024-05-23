import os
from src.scraper import remove_unneeded_docs


if __name__ == '__main__':
    dir_as_list = [f"./docs/{folder}" for folder in os.listdir("./links")]
    print(dir_as_list)
    remove_unneeded_docs(dir_as_list)
