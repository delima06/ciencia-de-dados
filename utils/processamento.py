%%writefile utils/processamento.py
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
palavras_vazias = set(stopwords.words('portuguese'))

def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'\W+', ' ', texto)
    todas_palavras = texto.split()
    
    palavras_validas = []
    for palavra in todas_palavras:
        if palavra not in palavras_vazias and len(palavra) > 2:
            palavras_validas.append(palavra)
            
    texto_final = " ".join(palavras_validas)
    return texto_final, palavras_validas
