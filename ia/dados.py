
from pathlib import Path
import re
import unicodedata

import pandas as pd


def ler_dados_treino():
    try:
        caminho_csv = Path(__file__).parent / "spam.csv"
        df = pd.read_csv(caminho_csv, encoding="utf-8")

        return df
    
    except:
        print("ler dados - treino.py deu erro")

#verifica os dados dentro do spam.csv
def verificar_dados_treino(texto):
    if texto is not None:
        print(texto.head())
        print(texto.info())
        #print("n de linhas:", len(dados))

    else:
        print("\n não foi possivel encontrar dados")

def limpar_dados_treino(texto):
    try:   
        texto = str(texto)
        texto = texto.lower()

        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")

        texto = re.sub(r"[^a-z0-9\s]", "", texto)

        return texto
    
    except:
        print("Erro no narmalizar_dados_treino -> treino.py")

def normalizar_dados_treino():
    try:
        dados = ler_dados_treino()

        dados = dados.drop_duplicates()
        
        dados["texto_limpo"] = dados["texto"].apply(limpar_dados_treino)
        
        return dados
    
    except:
        print("erro normalizar dados -> treino.py")


