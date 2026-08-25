%%writefile app.py
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from crochet import setup

# Importando as nossas funções da pasta utils
from utils.processamento import limpar_texto
from utils.raspagem_bs4 import raspar_com_bs4
from utils.raspagem_scrapy import raspar_com_scrapy

# Inicia o crochet
setup()

def criar_url_wiki(termo):
    termo_formatado = termo.strip().replace(" ", "_")
    return "https://pt.wikipedia.org/wiki/" + termo_formatado

st.title("Trabalho de Web Scraping: Wikipedia")

metodo_escolhido = st.radio("Escolha a biblioteca para extrair os dados:", ("Requests + BeautifulSoup", "Scrapy"))

termos_padrao = "Universidade Federal do Rio Grande do Norte, Ciência de Dados, Aprendizado de Máquina, Engenharia de Software, Armazém de Dados"
entrada_termos = st.text_area("Digite 5 termos separados por vírgula:", termos_padrao)
palavra_busca = st.text_input("Digite uma palavra para ver quantas vezes ela aparece (ex: software):")

if st.button("Iniciar Scraping"):
    lista_termos = entrada_termos.split(",")
    urls_para_raspar = []
    for termo in lista_termos:
        urls_para_raspar.append(criar_url_wiki(termo))

    st.write("Extraindo textos da Wikipedia, aguarde...")
    
    if metodo_escolhido == "Requests + BeautifulSoup":
        texto_bruto, tempo = raspar_com_bs4(urls_para_raspar)
    else:
        texto_bruto, tempo = raspar_com_scrapy(urls_para_raspar)

    st.success(f"Tempo demorado com {metodo_escolhido}: {tempo:.2f} segundos")

    if texto_bruto != "":
        texto_limpo, lista_palavras = limpar_texto(texto_bruto)
        
        st.subheader("Nuvem de Palavras")
        nuvem = WordCloud(width=800, height=400, background_color='white').generate(texto_limpo)
        figura, eixo = plt.subplots()
        eixo.imshow(nuvem, interpolation='bilinear')
        eixo.axis("off")
        st.pyplot(figura)
        
        st.subheader("Contagem de Palavra Específica")
        if palavra_busca != "":
            palavra_formatada = palavra_busca.lower().strip()
            quantidade = lista_palavras.count(palavra_formatada)
            st.write(f"A palavra **{palavra_formatada}** apareceu **{quantidade}** vezes no texto inteiro.")
    else:
        st.error("Nenhum texto foi encontrado.")
