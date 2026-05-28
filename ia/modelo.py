
from pathlib import Path
from ia.dados import limpar_dados_treino
import joblib

PASTA_MODELOS = Path(__file__).parent / "modelos"

#
#predição   
def prever_texto(texto, modelo, vetorizador):
    try:
        texto_limpo = limpar_dados_treino(texto)

        texto_vetorizado = vetorizador.transform([texto_limpo])
        resultado = modelo.predict(texto_vetorizado)

        #probabilidade = modelo.predict_proba(texto_vetorizado)

        #print("Probabilidade: ", probabilidade * 100)
        return resultado[0]

    except Exception as error:
        print("Erro em prever_texto -> Modelo.py")
        print("Erro Real: ", error)

        return None
    
    except Exception as error:
        print("Erro em prever_frase -> Modelo.py")
        print("Erro Real: ", error)

        return None
    
def prever_com_probabilidade(texto, modelo, vetorizador):
    try:
        texto_limpo = limpar_dados_treino(texto)

        texto_vetorizado = vetorizador.transform([texto_limpo])

        resultado = modelo.predict(texto_vetorizado)[0]

        probabilidades = modelo.predict_proba(texto_vetorizado)[0]

        classes = modelo.classes_

        indice_resultado = list(classes).index(resultado)

        probabilidade = probabilidades[indice_resultado]

        return resultado, float(probabilidade), classes, probabilidades

    except Exception as error:
        print("Erro no prever com probabilidade -> modelo.py")
        print("Error Real: ", error)
        return None

def carregar_modelo():
    try:
        caminho_modelo = PASTA_MODELOS / "modelo_adestrado.pkl"
        caminho_vetorizador = PASTA_MODELOS / "vetorizador.pkl"

        modelo = joblib.load(caminho_modelo)
        vetorizador = joblib.load(caminho_vetorizador)

        print("Modelo Carregado com sucesso")

        return modelo, vetorizador
        
    except Exception as error:
        print("Error ao carregar Modelo")
        print("Erro Real: ", error)

if __name__ == "__main__":
    modelo, vetorizador = carregar_modelo()

    if modelo is not None and vetorizador is not None:
        frase = "Clique agora para receber seu prêmio"

        resultado = prever_texto(frase, modelo, vetorizador)

        print("Frase:", frase)
        print("Classificação:", resultado)



