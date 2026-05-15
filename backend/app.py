import sys
from pathlib import Path
import sqlite3
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ_PROJETO))

from ia.modelo import prever_texto, carregar_modelo


# Caminho do banco
CAMINHO_BANCO = RAIZ_PROJETO / "database" / "banco.db"


# Inicialização
app = Flask(__name__)
CORS(app)


# Carregar modelo
modelo, vetorizador = carregar_modelo()

def padronizar_classificacao(classificacao):
    classificacao = classificacao.strip().lower()

    if classificacao in ["spam", "spams"]:
        return "SPAM"

    if classificacao in ["nao spam", "não spam", "nao_spam", "não_spam", "NAO_SPAM","ham", "normal"]:
        return "NÃO SPAM"

    return classificacao.upper()


@app.route("/")
def home():
    return "API Funcionando"


@app.route("/prever", methods=["POST"])
def prever_email():
    try:
        dados = request.get_json() or {}

        remetente = dados.get("remetente", "")
        assunto = dados.get("assunto", "")
        conteudo = dados.get("conteudo", "")

        texto_final = remetente + " " + assunto + " " + conteudo

        classificacao = prever_texto(texto_final, modelo, vetorizador)
        classificacao = padronizar_classificacao(classificacao)

        salvar_email(remetente, assunto, conteudo, classificacao)

        return jsonify({
            "status": "sucesso",
            "classificacao": classificacao
        }), 200

    except Exception as error:
        print("Erro na rota /prever:", error)

        return jsonify({
            "status": "erro",
            "erro": "Erro na rota prever",
            "detalhe": str(error)
        }), 400


@app.route("/dashboard", methods=["GET"])
def dashboard():
    try:
        conexao = sqlite3.connect(CAMINHO_BANCO)
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM emails")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM emails WHERE UPPER(classificacao) = 'SPAM'")
        spam = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM emails WHERE UPPER(classificacao) = 'NÃO SPAM'")
        nao_spam = cursor.fetchone()[0]

        cursor.execute("SELECT data_hora FROM emails ORDER BY id DESC LIMIT 1")
        ultima = cursor.fetchone()

        conexao.close()

        ultima_verificacao = ultima[0] if ultima else "--:--"

        return jsonify({
            "emails_analisados": total,
            "spam_detectados": spam,
            "nao_spam": nao_spam,
            "ultima_verificacao": ultima_verificacao
        }), 200

    except Exception as error:
        print("Erro na rota /dashboard:", error)

        return jsonify({
            "status": "erro",
            "erro": "Erro ao carregar dashboard",
            "detalhe": str(error)
        }), 400


@app.route("/emails", methods=["GET"])
def listar_emails():
    try:
        conexao = sqlite3.connect(CAMINHO_BANCO)
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT remetente, assunto, classificacao, data_hora
            FROM emails
            ORDER BY id DESC
            LIMIT 10
        """)

        resultados = cursor.fetchall()
        conexao.close()

        emails = []

        for item in resultados:
            emails.append({
                "remetente": item[0],
                "assunto": item[1],
                "classificacao": item[2],
                "data_hora": item[3]
            })

        return jsonify(emails), 200

    except Exception as error:
        print("Erro na rota /emails:", error)

        return jsonify({
            "status": "erro",
            "erro": "Erro ao listar e-mails",
            "detalhe": str(error)
        }), 400


@app.route("/conectar-email", methods=["POST"])
def conectar_email():
    try:
        dados = request.get_json() or {}

        email = dados.get("email")
        servidor = dados.get("servidor")
        porta = dados.get("porta")

        return jsonify({
            "status": "sucesso",
            "mensagem": "E-mail conectado com sucesso!",
            "email": email,
            "servidor": servidor,
            "porta": porta
        }), 200

    except Exception as error:
        print("Erro na rota /conectar-email:", error)

        return jsonify({
            "status": "erro",
            "erro": "Erro ao conectar e-mail",
            "detalhe": str(error)
        }), 400


def salvar_email(remetente, assunto, conteudo, classificacao):
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
        INSERT INTO emails (remetente, assunto, conteudo, classificacao, data_hora)
        VALUES (?, ?, ?, ?, ?)
    """, (remetente, assunto, conteudo, classificacao, data_hora))

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    app.run(debug=True)