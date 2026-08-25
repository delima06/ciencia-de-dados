# Web Scraping com Wikipedia (Streamlit App)

Trabalho prático de ingestão de dados não estruturados via Web Scraping em páginas da Wikipedia, com geração de nuvem de palavras e análise de frequência de termos.

## 📁 Estrutura do Projeto
- `app.py`: Interface da aplicação em Streamlit e orquestração do fluxo.
- `utils/`: Módulos com a lógica desacoplada do projeto:
  - `raspagem_bs4.py`: Implementação do web scraping com `requests` + `BeautifulSoup4`.
  - `raspagem_scrapy.py`: Implementação com `Scrapy` + `Crochet` para execução assíncrona desacoplada.
  - `processamento.py`: Limpeza de texto, remoção de caracteres especiais e filtragem de *stopwords* via NLTK.
- `requirements.txt`: Dependências do projeto.
- `README.md`: Documentação.

## 🛠️ Tecnologias
- Python 3
- Streamlit
- Requests & BeautifulSoup4
- Scrapy & Crochet
- NLTK
- WordCloud & Matplotlib

## 🚀 Como Executar
```bash
pip install -r requirements.txt
streamlit run app.py
