
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from ia.dados import normalizar_dados_treino

#Leitor do .csv com pandas
def vetorizar_dados_treino(dados):
    try:
        vetoriador = CountVectorizer()

        x = vetoriador.fit_transform(dados["texto_limpo"])
        y = dados["categoria"]

        return x, y, vetoriador


    except:
        print("Erro em vetorizar_dados_treino -> treino.py")

def treinar_modelo():
    try:
        x, y, vetorizador = preparar_dados_treino()

        modelo = MultinomialNB()
        modelo.fit(x, y)
        print("Modelo Treinado!")

        return modelo, vetorizador

    except Exception as error:
        print("Erro em treinar modelo -> Modelo.py")
        print("Erro Real: ", error)

        return None

def preparar_dados_treino():
    dados = normalizar_dados_treino()

    if dados is None:
        return None, None, None

    X, y, vetorizador = vetorizar_dados_treino(dados)

    return X, y, vetorizador

def salvar_modelo():
    try:
        modelo, vetorizador = treinar_modelo()
        PASTA_MODELOS = Path(__file__).parent / "modelos"

        if modelo is None or vetorizador is None:
            print("Error salvar modelo: não treinado corretamente")
            return
        
        PASTA_MODELOS.mkdir(exist_ok=True)

        caminho_modelo = PASTA_MODELOS / "modelo_adestrado.pkl"
        caminho_vetorizador = PASTA_MODELOS / "vetorizador.pkl"

        joblib.dump(modelo, caminho_modelo)
        joblib.dump(vetorizador, caminho_vetorizador)

        print("Modelo salvo com sucesso!")
        print(f"Arquivo criado: {caminho_modelo}")
        print(f"Arquivo criado: {caminho_vetorizador}")
        
    except Exception as error:
        print("Erro salvar modelo -> modelo.py")
        print("Erro Real: ", error)
        
        return None


dados_normal = normalizar_dados_treino()

if dados_normal is not None:
    x, y, vetorizador = vetorizar_dados_treino(dados_normal)


if __name__ == "__main__":
    X, y, vetorizador = preparar_dados_treino()

    # if X is not None:
    #     print("\nTreino.py funcionando corretamente!")
    #     print("Formato de X:", X.shape)
    #     print("Categorias:")
    #     print(y.value_counts())
    #     print("Vocabulário:")
    #     print(vetorizador.get_feature_names_out())