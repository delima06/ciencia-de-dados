%%writefile app.py
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from crochet import setup

# Importando as funcoes da pasta utils
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

entrada_termos = st.text_area(
    "Digite 5 termos separados por vírgula:", 
    placeholder="Ex: Inteligência Artificial, Banco de Dados, Redes de Computadores, Segurança da Informação, Algoritmo"
)
palavra_busca = st.text_input(
    "Digite uma palavra para ver a frequência:", 
    placeholder="Ex: dados"
)

if st.button("Iniciar Scraping"):
    if not entrada_termos.strip():
        st.warning("Por favor, digite os termos separados por vírgula antes de iniciar.")
    else:
        lista_termos = [t.strip() for t in entrada_termos.split(",") if t.strip()]
        
        if len(lista_termos) != 5:
            st.info(f"Você digitou {len(lista_termos)} termo(s). O ideal para a atividade são 5 termos.")
            
        urls_para_raspar = [criar_url_wiki(termo) for termo in lista_termos]

        st.write("Extraindo textos da Wikipedia, aguarde...")
        
        if metodo_escolhido == "Requests + BeautifulSoup":
            texto_bruto, tempo = raspar_com_bs4(urls_para_raspar)
        else:
            texto_bruto, tempo = raspar_com_scrapy(urls_para_raspar)

        st.success(f"Tempo demorado com {metodo_escolhido}: {tempo:.2f} segundos")

        if texto_bruto.strip() != "":
            texto_limpo, lista_palavras = limpar_texto(texto_bruto)
            
            st.subheader("Nuvem de Palavras")
            nuvem = WordCloud(width=800, height=400, background_color='white').generate(texto_limpo)
            figura, eixo = plt.subplots()
            eixo.imshow(nuvem, interpolation='bilinear')
            eixo.axis("off")
            st.pyplot(figura)
            
            st.subheader("Contagem de Palavra Específica")
            if palavra_busca.strip() != "":
                palavra_formatada = palavra_busca.lower().strip()
                quantidade = lista_palavras.count(palavra_formatada)
                st.write(f"A palavra **{palavra_formatada}** apareceu **{quantidade}** vezes no texto consolidado.")
            else:
                st.info("Nenhuma palavra foi informada para contagem.")
        else:
            st.error("Nenhum texto foi encontrado nas páginas informadas. Verifique a ortografia dos termos.")
