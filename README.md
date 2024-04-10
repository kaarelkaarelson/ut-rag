# ut_rag

RAG Application for ut.ee domain.

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

## Tutorials

Qdrant setup:

https://qdrant.tech/documentation/quick-start/

Llamaindex with Qdrant:

https://docs.llamaindex.ai/en/stable/examples/vector_stores/QdrantIndexDemo.html

Run open-source models with Ollama using free GPU

[https://github.com/kaarelkaarelson/colab_ollama](https://github.com/kaarelkaarelson/colab_ollama)
