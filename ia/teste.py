
from modelo import prever_texto, prever_com_probabilidade
from treino import treinar_modelo
teste = [
   ("você ganhou um prêmio para viajar até Maldivas", "spam"),
]

def testar_modelo():
    try:
        modelo, vetorizador = treinar_modelo()
        
        acertos = 0
        erros = []

        print("Testando modelo")
        print("-" * 40)

        for linha, (frase, esperado) in enumerate(teste, start=1):
            resultado = prever_texto(frase, modelo,vetorizador)

            if resultado == esperado:
                acertos += 1

            else:
                resultado, probabilidade, classes, probabilidades = prever_com_probabilidade(
                    frase,
                    modelo,
                    vetorizador
                )

                erros.append((linha, frase, esperado, resultado, classes, probabilidades))

        total = len(teste)

        probabilidade_error = ((total-acertos)/total) * 100
        probabilidade_acerto = (acertos/total) * 100

        print(f"Erros: {probabilidade_error:.2f}%")
        print(f"Prob. Acertos: {probabilidade_acerto:.2f}%\n")

        for linha, frase, esperado, resultado, classes, probabilidades in erros:
            print(f"{linha}. Entrada: {frase}")
            print(f"Esperado: {esperado}")
            print(f"Resultado: {resultado}")


            for classes, probabilidade in zip(classes, probabilidades):
               print(f"{classes}: {probabilidade * 100:.2f}%")
 
            print("-"*40)

    except Exception as error:
        print("Erro teste_modelo -> teste.py")
        print("Erro real: ", error)

        return None
    
if __name__=="__main__":
    testar_modelo()