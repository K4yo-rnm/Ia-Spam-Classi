

from pathlib import Path

from flask import jsonify, request

from ia.modelo import prever_texto, carregar_modelo

from datetime import datetime

from backend.services.email_services import (
    testar_conexao_imap,
    buscar_ultimos_emails_imap,
    mover_email_para_spam
)

from backend.services.dashboard_services import obter_dashboard
from backend.services.ia_services import padronizar_classificacao

from backend.services.banco_services import (
    salvar_email,
    listar_utlimos_emails,
    email_ja_existe
)

from backend.services.config_server import (
    carregar_configuracoes,
    salvar_configuracoes
)

from flask import redirect, session, request, jsonify
from services.google_auth_service import (
    criar_fluxo_google,
    salvar_credenciais_google,
    google_esta_conectado,
    desconectar_google
)

from services.gmail_api_service import (
    buscar_ultimos_emails_gmail_api,
    mover_email_para_spam_gmail_api
)


RAIZ_PROJETO = Path(__file__).resolve().parent.parent


modelo, vetorizador = carregar_modelo()

def registrar_rotas(app):

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
            dados_dashboard = obter_dashboard()

            return jsonify(dados_dashboard), 200

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
            emails = listar_utlimos_emails(10)

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
            senha = dados.get("senha")
            servidor = dados.get("servidor")
            porta = dados.get("porta", 993)

            conectado, mensagem = testar_conexao_imap(
                email,
                senha,
                servidor,
                porta
            )

            if conectado:
                return jsonify({
                    "status": "sucesso",
                    "mensagem": "E-mail conectado com sucesso!",
                    "email": email,
                    "servidor": servidor,
                    "porta": porta
                }), 200
            
            return jsonify({
                "status": "erro",
                "mensagem": mensagem
            }), 400

        except Exception as error:
            print("Erro na rota /conectar-email:", error)

            return jsonify({
                "status": "erro",
                "erro": "Erro ao conectar e-mail",
                "detalhe": str(error)
            }), 500
        
    @app.route("/buscar-emails", methods=["POST"])
    def buscar_emails():
        try:
            dados = request.get_json() or {}

            email_usuario = dados.get("email")
            senha = dados.get("senha")
            servidor = dados.get("servidor")
            porta = dados.get("porta", 993)
            limite = dados.get("limite", 5)

            configuracoes = carregar_configuracoes()
            apenas_nao_lidos = configuracoes.get("analisar_nao_lidos", True)

            sucesso, mensagem, emails = buscar_ultimos_emails_imap(
                email_usuario,
                senha,
                servidor,
                porta,
                limite,
                apenas_nao_lidos
            )

            if sucesso:
                return jsonify({
                    "status": "sucesso",
                    "mensagem": mensagem,
                    "emails": emails
                }), 200

            return jsonify({
                "status": "erro",
                "mensagem": mensagem,
                "emails": []
            }), 400

        except Exception as error:
            print("Erro na rota /buscar-emails:", error)

            return jsonify({
                "status": "erro",
                "mensagem": "Erro interno ao buscar e-mails.",
                "detalhe": str(error)
            }), 500
        
    @app.route("/analisar-emails", methods=["POST"])
    def analisar_emails():
        try:
            dados = request.get_json() or {}

            email_usuario = dados.get("email")
            senha = dados.get("senha")
            servidor = dados.get("servidor")
            porta = dados.get("porta", 993)
            limite = dados.get("limite", 5)

            print("===== DADOS RECEBIDOS NA ROTA /analisar-emails =====")
            print("DADOS BODY:", dados)
            print("EMAIL:", email_usuario)
            print("SENHA:", senha)
            print("SERVIDOR:", servidor)
            print("PORTA:", porta)
            print("===================================================")

            configuracoes = carregar_configuracoes()
            apenas_nao_lidos = configuracoes.get("analisar_nao_lidos", True)
            mover_spam = configuracoes.get("mover_spam", False)

            sucesso, mensagem, emails = buscar_ultimos_emails_imap(
                email_usuario,
                senha,
                servidor,
                porta,
                limite,
                apenas_nao_lidos
            )

            if not sucesso:
                return jsonify({
                    "status": "erro",
                    "mensagem": mensagem
                }), 400

            emails_analisados = []
            emails_repetidos = []

            for email_item in emails:
                email_id = email_item.get("email_uid")
                remetente = email_item.get("remetente", "")
                assunto = email_item.get("assunto", "")
                conteudo = email_item.get("conteudo", "")
                data_email = email_item.get("data", "")

                if email_ja_existe(email_id):
                    emails_repetidos.append({
                        "remetente":remetente,
                        "assunto":assunto,
                        "motivo": "E-mail já analisado anteriormente"
                    })
                    continue

                texto_final = remetente + " " + assunto + " " + conteudo

                classificacao = prever_texto(texto_final, modelo, vetorizador)
                classificacao = padronizar_classificacao(classificacao)

                salvar_email(remetente, assunto, conteudo, classificacao, email_id, data_email)

                movido_para_spam = False
                mensagem_movimento = ""

                if mover_spam and classificacao == "SPAM":
                    sucesso_movimento, mensagem_movimento = mover_email_para_spam(
                        email_usuario,
                        senha,
                        servidor,
                        porta,
                        email_id
                    )

                    movido_para_spam = sucesso_movimento

                    print("MOVER PARA SPAM:", sucesso_movimento)
                    print("MENSAGEM:", mensagem_movimento)

                emails_analisados.append({
                    "remetente": remetente,
                    "assunto": assunto,
                    "data": email_item.get("data", ""),
                    "classificacao": classificacao,
                    "movido_para_spam": movido_para_spam,
                    "mensagem_movimento": mensagem_movimento
                })

            configuracoes["ultima_verificacao"] = datetime.now().strftime("%d/%m/%Y %H:%M" )
            salvar_configuracoes(configuracoes)

            return jsonify({
                "status": "sucesso",
                "mensagem": "Análise concluída!",
                "novos_analisados": len(emails_analisados),
                "repetidos_ignorados": len(emails_repetidos),
                "emails_analisados": emails_analisados,
                "emails_repetidos": emails_repetidos
            }), 200

        except Exception as error:
            print("Erro na rota /analisar-emails:", error)

            return jsonify({
                "status": "erro",
                "mensagem": "Erro interno ao analisar e-mails.",
                "detalhe": str(error)
            }), 500
        
    @app.route("/configuracoes", methods=["GET"])
    def obter_configuracoes():
        try:
            configuracoes = carregar_configuracoes()

            return jsonify({
                "status": "sucesso",
                "configuracoes": configuracoes
            }), 200

        except Exception as error:
            print("Erro ao carregar configurações:", error)

            return jsonify({
                "status": "erro",
                "mensagem": "Erro ao carregar configurações.",
                "detalhe": str(error)
            }), 500

    @app.route("/configuracoes", methods=["POST"])
    def salvar_configuracoes_rota():
        try:
            dados = request.get_json() or {}

            configuracoes = {
                "intervalo": dados.get("intervalo", "5"),
                "analisar_nao_lidos": dados.get("analisar_nao_lidos", True),
                "marcar_lidos": dados.get("marcar_lidos", False),
                "mover_spam": dados.get("mover_spam", False),
                "notificacoes": dados.get("notificacoes", True),
                "notificacao_area": dados.get("notificacao_area", True),
                "idioma": dados.get("idioma", "pt-BR"),
                "tema": dados.get("tema", "claro")
            }

            salvar_configuracoes(configuracoes)

            return jsonify({
                "status": "sucesso",
                "mensagem": "Configurações salvas com sucesso!",
                "configuracoes": configuracoes
            }), 200

        except Exception as error:
            print("Erro ao salvar configurações:", error)

            return jsonify({
                "status": "erro",
                "mensagem": "Erro ao salvar configurações.",
                "detalhe": str(error)
            }), 500
        
    @app.route("/login-google", methods=["GET"])
    def login_google():
        flow = criar_fluxo_google()

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent"
        )

        session["google_oauth_state"] = state
        session["google_code_verifier"] = flow.code_verifier

        return redirect(authorization_url)

    @app.route("/callback-google", methods=["GET"])
    def callback_google():
        try:
            state = session.get("google_oauth_state")
            code_verifier = session.get("google_code_verifier")

            flow = criar_fluxo_google()
            flow.code_verifier = code_verifier

            flow.fetch_token(authorization_response=request.url)

            credentials = flow.credentials

            salvar_credenciais_google(credentials)

            return redirect("http://127.0.0.1:5500/frontend/index.html?google=conectado")

        except Exception as erro:
            print("Erro no callback do Google:", erro)

            return jsonify({
                "status": "erro",
                "mensagem": "Erro ao conectar com Google.",
                "detalhe": str(erro)
            }), 500

    @app.route("/status-google", methods=["GET"])
    def status_google():
        conectado = google_esta_conectado()

        return jsonify({
            "status": "sucesso",
            "conectado": conectado
        }), 200

    @app.route("/desconectar-google", methods=["POST"])
    def rota_desconectar_google():
        desconectar_google()

        return jsonify({
            "status": "sucesso",
            "mensagem": "Conta Google desconectada com sucesso."
        }), 200

    @app.route("/analisar-emails-google", methods=["POST"])
    def analisar_emails_google():
        try:
            dados = request.get_json() or {}

            limite = dados.get("limite", 10)

            configuracoes = carregar_configuracoes()
            apenas_nao_lidos = configuracoes.get("analisar_nao_lidos", True)
            mover_spam = configuracoes.get("mover_spam", False)

            sucesso, mensagem, emails = buscar_ultimos_emails_gmail_api(
                limite,
                apenas_nao_lidos
            )

            if not sucesso:
                return jsonify({
                    "status": "erro",
                    "mensagem": mensagem
                }), 400

            emails_analisados = []
            emails_repetidos = []
            total_movidos_spam = 0

            for email_item in emails:
                email_id = email_item.get("email_uid")
                gmail_message_id = email_item.get("gmail_message_id")

                remetente = email_item.get("remetente", "")
                assunto = email_item.get("assunto", "")
                conteudo = email_item.get("conteudo", "")
                data_email = email_item.get("data", "")

                if email_ja_existe(email_id):
                    emails_repetidos.append({
                        "remetente": remetente,
                        "assunto": assunto,
                        "motivo": "E-mail já analisado anteriormente"
                    })
                    continue

                texto_final = remetente + " " + assunto + " " + conteudo

                classificacao = prever_texto(texto_final, modelo, vetorizador)
                classificacao = padronizar_classificacao(classificacao)

                salvar_email(
                    remetente,
                    assunto,
                    conteudo,
                    classificacao,
                    email_id,
                    data_email
                )

                movido_para_spam = False
                mensagem_movimento = ""

                if mover_spam and classificacao == "SPAM":
                    sucesso_movimento, mensagem_movimento = mover_email_para_spam_gmail_api(
                        gmail_message_id
                    )

                    movido_para_spam = sucesso_movimento

                    if sucesso_movimento:
                        total_movidos_spam += 1

                emails_analisados.append({
                    "remetente": remetente,
                    "assunto": assunto,
                    "data": data_email,
                    "classificacao": classificacao,
                    "movido_para_spam": movido_para_spam,
                    "mensagem_movimento": mensagem_movimento
                })

            configuracoes["ultima_verificacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            salvar_configuracoes(configuracoes)

            return jsonify({
                "status": "sucesso",
                "mensagem": "Análise concluída pela Gmail API!",
                "novos_analisados": len(emails_analisados),
                "repetidos_ignorados": len(emails_repetidos),
                "movidos_para_spam": total_movidos_spam,
                "emails_analisados": emails_analisados,
                "emails_repetidos": emails_repetidos
            }), 200

        except Exception as erro:
            print("Erro na rota /analisar-emails-google:", erro)

            return jsonify({
                "status": "erro",
                "mensagem": "Erro interno ao analisar e-mails com Google.",
                "detalhe": str(erro)
            }), 500
