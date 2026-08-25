%%writefile utils/raspagem_bs4.py
import requests
from bs4 import BeautifulSoup
import time

def raspar_com_bs4(lista_urls):
    tempo_inicio = time.time()
    texto_total = ""
    
    for url in lista_urls:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.content, 'html.parser')
            paragrafos = sopa.find_all('p')
            for p in paragrafos:
                texto_total = texto_total + p.get_text() + " "
                
    tempo_fim = time.time()
    return texto_total, tempo_fim - tempo_inicio
