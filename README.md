# UT RAG

Retrieval Augmented Generation Chatbot for the University of Tartu.

## Setup

**Virtual Environment**

Create virtual environment for the project. Make sure you have an updated version of conda.

`conda env create -f environment.yml`

Activate conda environment

`conda activate ut-rag`

**Install packages**

`pip install -r requirements.txt`

`pip install -e .`

**Webscrape and download pages**

`python -m scripts.crawl_subdomains`

`python -m scripts.clean_links`

`python -m scripts.download_links`


**Run**

`python -m scripts.run_app`

## Spider

Activate the spider (NB! Only activate with supervision, check the 'ut/ut_links.txt file')

`scrapy crawl subdomains`

## Tutorials

Run open-source models with Ollama using free GPU

[https://github.com/kaarelkaarelson/colab_ollama](https://github.com/kaarelkaarelson/colab_ollama)

## Documents

NB! There are .pdf and .docx as sites in ut.ee domain.
