import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def raspar_com_bs4(lista_urls):
    tempo_inicio = time.time()
    texto_total = ""
    
    for url in lista_urls:
        try:
            resposta = requests.get(url, headers=HEADERS, timeout=10)
            if resposta.status_code == 200:
                sopa = BeautifulSoup(resposta.content, 'html.parser')
                paragrafos = sopa.find_all('p')
                for p in paragrafos:
                    texto_total = texto_total + p.get_text() + " "
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")
                
    tempo_fim = time.time()
    return texto_total, tempo_fim - tempo_inicio
