

from ia.modelo import prever_texto, carregar_modelo
from flask import Flask, jsonify, request
from flask_cors import CORS 

#Inicialização
app = Flask(__name__)
CORS(app)

#carregarModelo
modelo, vetorizador = carregar_modelo()

#Criar rota teste
@app.route('/')
def home():
    return "API Funcionando"

@app.route("/prever", methods=['POST'])
def prever():
    try:
        dados = request.get_json()
        texto = dados['texto']

        resultado = prever_texto(texto, modelo, vetorizador)

        return jsonify({
            "resultado": resultado
        })
    
    except Exception as error:
        print("Erro na rota /prever:", error)

        return jsonify({
            "erro": "Erro na rota prever"
        }), 400



if __name__ == "__main__":
    app.run(debug=True)