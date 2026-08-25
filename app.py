%%writefile app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerRunner
from crochet import setup, wait_for
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import re

setup()

nltk.download('stopwords', quiet=True)
palavras_vazias = set(stopwords.words('portuguese'))

# Função para montar o link da Wikipedia
def criar_url_wiki(termo):
    # Tira os espaços das pontas e troca os espaços do meio por underline
    termo_formatado = termo.strip().replace(" ", "_")
    url = "https://pt.wikipedia.org/wiki/" + termo_formatado
    return url

# Função para limpar o texto
def limpar_texto(texto):
    texto = texto.lower() # Tudo minúsculo
    texto = re.sub(r'\W+', ' ', texto) # Tira pontuações
    todas_palavras = texto.split() # Separa em uma lista de palavras
    
    palavras_validas = []
    for palavra in todas_palavras:
        if palavra not in palavras_vazias and len(palavra) > 2:
            palavras_validas.append(palavra)
            
    texto_final = " ".join(palavras_validas)
    return texto_final, palavras_validas

def raspar_com_bs4(lista_urls):
    tempo_inicio = time.time()
    texto_total = ""
    
    for url in lista_urls:
        resposta = requests.get(url)
        if resposta.status_code == 200: # 200 = OK
            sopa = BeautifulSoup(resposta.content, 'html.parser')
            paragrafos = sopa.find_all('p')
            
            for p in paragrafos:
                texto_total = texto_total + p.get_text() + " "
                
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    return texto_total, tempo_execucao

class SpiderWikipedia(scrapy.Spider):
    name = "wiki_spider"
    
    def __init__(self, start_urls, lista_textos, *args, **kwargs):
        super(SpiderWikipedia, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.lista_textos = lista_textos

    def parse(self, response):
        paragrafos = response.css('p::text').getall()
        texto_junto = " ".join(paragrafos)
        self.lista_textos.append(texto_junto)

@wait_for(timeout=60.0)
def rodar_spider(urls, lista_textos):
    runner = CrawlerRunner()
    return runner.crawl(SpiderWikipedia, start_urls=urls, lista_textos=lista_textos)

def raspar_com_scrapy(lista_urls):
    tempo_inicio = time.time()
    lista_de_textos = []
    
    rodar_spider(lista_urls, lista_de_textos)
    
    texto_total = " ".join(lista_de_textos)
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    
    return texto_total, tempo_execucao


st.title("Trabalho de Web Scraping: Wikipedia")

metodo_escolhido = st.radio(
    "Escolha a biblioteca para extrair os dados:", 
    ("Requests + BeautifulSoup", "Scrapy")
)

# Entrada dos termos
termos_padrao = "Universidade Federal do Rio Grande do Norte, Ciência de Dados, Aprendizado de Máquina, Engenharia de Software, Armazém de Dados"
entrada_termos = st.text_area("Digite 5 termos separados por vírgula:", termos_padrao)

# Palavra para buscar
palavra_busca = st.text_input("Digite uma palavra para ver quantas vezes ela aparece (ex: dados):")

# Botão principal
if st.button("Iniciar Scraping"):
    
    # Prepara as URLs baseadas nos termos digitados
    lista_termos = entrada_termos.split(",")
    urls_para_raspar = []
    for termo in lista_termos:
        url = criar_url_wiki(termo)
        urls_para_raspar.append(url)

    st.write("Extraindo textos da Wikipedia, aguarde...")
    
    # Executa a raspagem dependendo da escolha
    if metodo_escolhido == "Requests + BeautifulSoup":
        texto_bruto, tempo = raspar_com_bs4(urls_para_raspar)
    else:
        texto_bruto, tempo = raspar_com_scrapy(urls_para_raspar)

    st.success(f"Tempo demorado com {metodo_escolhido}: {tempo:.2f} segundos")

    # Só continua se tiver achado texto
    if texto_bruto != "":
        texto_limpo, lista_palavras = limpar_texto(texto_bruto)
        
        st.subheader("Nuvem de Palavras")
        nuvem = WordCloud(width=800, height=400, background_color='white').generate(texto_limpo)
        
        figura, eixo = plt.subplots()
        eixo.imshow(nuvem, interpolation='bilinear')
        eixo.axis("off") # Tira as bordas e números do gráfico
        st.pyplot(figura)
        
        st.subheader("Contagem de Palavra Específica")
        if palavra_busca != "":
            palavra_formatada = palavra_busca.lower().strip()
            quantidade = lista_palavras.count(palavra_formatada)
            st.write(f"A palavra **{palavra_formatada}** apareceu **{quantidade}** vezes no texto inteiro.")
        else:
            st.write("Você não digitou nenhuma palavra para pesquisar.")
    else:
        st.error("Nenhum texto foi encontrado. Verifique se os termos estão corretos.")
