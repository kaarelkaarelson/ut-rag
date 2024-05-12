# UT RAG

Retrieval Augmented Generation Chatbot for the University of Tartu domain

## Setup

**Virtual Environment**

Create virtual environment for the project

`py -3.11 -m venv .venv` _NB! Use python version 3.11.X_

Activate virtual environment

`.venv\Scripts\activate`

_For more info on python virtual environments https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/_

**Install packages**

Make sure virtual environment is activated

Prepare pip

`py -m pip install --upgrade pip`

Install all packages

`py -m pip install -r requirements.txt`

**Run**

`python -m streamlit run .\app.py`

## Spider

Activate the spider (NB! Only activate with supervision, check the 'ut/ut_links.txt file')

`scrapy crawl subdomains`

## Tutorials

Run open-source models with Ollama using free GPU

[https://github.com/kaarelkaarelson/colab_ollama](https://github.com/kaarelkaarelson/colab_ollama)

## Documents

NB! There are .pdf and .docx as sites in ut.ee domain.
