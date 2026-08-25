import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from crochet import wait_for
import time

class SpiderWikipedia(scrapy.Spider):
    name = "wiki_spider"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'LOG_LEVEL': 'ERROR',
        'TWISTED_REACTOR': 'twisted.internet.epollreactor.EPollReactor'
    }
    
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
    config = Settings()
    config.set('TWISTED_REACTOR', 'twisted.internet.epollreactor.EPollReactor')
    config.set('LOG_LEVEL', 'ERROR')
    runner = CrawlerRunner(config)
    return runner.crawl(SpiderWikipedia, start_urls=urls, lista_textos=lista_textos)

def raspar_com_scrapy(lista_urls):
    tempo_inicio = time.time()
    lista_de_textos = []
    rodar_spider(lista_urls, lista_de_textos)
    texto_total = " ".join(lista_de_textos)
    tempo_fim = time.time()
    return texto_total, tempo_fim - tempo_inicio
