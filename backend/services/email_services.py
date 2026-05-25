

import imaplib
from email.utils import parsedate_to_datetime
from datetime import datetime
from zoneinfo import ZoneInfo

def testar_conexao_imap(email_usuario, senha, servidor, porta):
    """
    Testa a conexão IMAP com Gmail, Outlook ou outro provedor.

    email_usuario: e-mail completo do usuário
    senha: senha de aplicativo ou senha permitida pelo provedor
    servidor: servidor IMAP, exemplo: imap.gmail.com
    porta: porta IMAP, geralmente 993
    """

    try:
        if not email_usuario or not senha or not servidor:
            return False, "Preencha e-mail, senha e servidor IMAP."

        porta = int(porta)

        conexao = imaplib.IMAP4_SSL(servidor, porta)
        conexao.login(email_usuario, senha)
        conexao.logout()

        return True, "Conexão IMAP realizada com sucesso!"

    except imaplib.IMAP4.error as erro:
        return False, f"Erro de autenticação IMAP: {erro}"

    except ValueError:
        return False, "A porta precisa ser um número válido."

    except Exception as erro:
        return False, f"Erro ao conectar via IMAP: {erro}"
    
import imaplib
import email
import re

from email.header import decode_header


def decodificar_texto(texto):
    """
    Decodifica textos de cabeçalhos de e-mail, como assunto e remetente.
    Alguns e-mails vêm com caracteres codificados.
    """

    if texto is None:
        return ""

    try:
        partes = decode_header(texto)
        resultado = ""

        for parte, codificacao in partes:
            if isinstance(parte, bytes):
                resultado += parte.decode(codificacao or "utf-8", errors="ignore")
            else:
                resultado += parte

        return resultado

    except Exception:
        return str(texto)


def limpar_html(texto):
    """
    Remove tags HTML simples do corpo do e-mail.
    Isso ajuda quando o e-mail vem em formato HTML.
    """

    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def extrair_corpo_email(mensagem):
    """
    Extrai o conteúdo principal do e-mail.
    Dá preferência para text/plain.
    Se não encontrar, tenta pegar text/html e limpar as tags.
    """

    corpo_texto = ""
    corpo_html = ""

    if mensagem.is_multipart():
        for parte in mensagem.walk():
            tipo_conteudo = parte.get_content_type()
            disposicao = str(parte.get("Content-Disposition"))

            if "attachment" in disposicao:
                continue

            try:
                payload = parte.get_payload(decode=True)

                if payload is None:
                    continue

                charset = parte.get_content_charset() or "utf-8"
                texto = payload.decode(charset, errors="ignore")

                if tipo_conteudo == "text/plain" and not corpo_texto:
                    corpo_texto = texto

                elif tipo_conteudo == "text/html" and not corpo_html:
                    corpo_html = limpar_html(texto)

            except Exception:
                continue

    else:
        try:
            payload = mensagem.get_payload(decode=True)
            charset = mensagem.get_content_charset() or "utf-8"

            if payload:
                texto = payload.decode(charset, errors="ignore")

                if mensagem.get_content_type() == "text/html":
                    corpo_html = limpar_html(texto)
                else:
                    corpo_texto = texto

        except Exception:
            pass

    if corpo_texto:
        return corpo_texto.strip()

    return corpo_html.strip()

def formatar_data_email(data_email):
    """
    Converte a data original do e-mail para o formato brasileiro:
    dd/mm/aaaa hh:mm
    """

    if not data_email:
        return datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        data_convertida = parsedate_to_datetime(data_email)

        if data_convertida.tzinfo is None:
            data_convertida = data_convertida.replace(tzinfo=ZoneInfo("UTC"))

        data_brasil = data_convertida.astimezone(ZoneInfo("America/Sao_Paulo"))

        return data_brasil.strftime("%d/%m/%Y %H:%M")

    except Exception as erro:
        print("Erro ao formatar data do e-mail:", erro)
        return data_email

def buscar_ultimos_emails_imap(email_usuario, senha, servidor, porta, limite=5, apenas_nao_lidos=True):
    try:
        porta = int(porta)
        limite = int(limite)

        print("===== TESTE DE CONEXÃO IMAP =====")
        print("EMAIL:", email_usuario)
        print("SERVIDOR:", servidor)
        print("PORTA:", porta)
        print("LIMITE:", limite)
        print("APENAS NÃO LIDOS:", apenas_nao_lidos)
        print("================================")

        conexao = imaplib.IMAP4_SSL(servidor, porta)
        conexao.login(email_usuario, senha)

        conexao.select("INBOX", readonly=True)

        criterio_busca = "UNSEEN" if apenas_nao_lidos else "ALL"
        print("Criterio de busca: ", criterio_busca)
        status, dados = conexao.uid("search", None, criterio_busca)

        if status != "OK":
            conexao.logout()
            return False, "Erro ao buscar e-mails.", []

        uids_emails = dados[0].split()
        ultimos_uids = uids_emails[-limite:]

        emails = []

        for uid_email in reversed(ultimos_uids):

            uid_texto = uid_email.decode("utf-8", errors="ignore")

            status_fetch, dados_email = conexao.uid("fetch", uid_texto, "(RFC822)")

            if status_fetch != "OK":
                continue

            email_uid = f"{email_usuario}:{servidor}:INBOX:{uid_texto}"

            for resposta in dados_email:
                if isinstance(resposta, tuple):
                    mensagem = email.message_from_bytes(resposta[1])

                    remetente = decodificar_texto(mensagem.get("From"))
                    assunto = decodificar_texto(mensagem.get("Subject"))

                    data = decodificar_texto(mensagem.get("Date"))
                    data_formatada = formatar_data_email(data)
                    
                    conteudo = extrair_corpo_email(mensagem)

                    emails.append({
                        "email_uid": email_uid,
                        "remetente": remetente,
                        "assunto": assunto,
                        "data": data_formatada,
                        "conteudo": conteudo[:1000]
                    })

        conexao.logout()

        print("TOTAL RETORNADO PARA API:", len(emails))

        return True, "E-mails buscados com sucesso!", emails

    except imaplib.IMAP4.error as erro:
        return False, f"Erro de autenticação IMAP: {erro}", []

    except Exception as erro:
        return False, f"Erro ao buscar e-mails via IMAP: {erro}", []
    
def mover_email_para_spam(email_usuario, senha, servidor, porta, email_uid):
    try:
        porta = int(porta)

        if not email_uid:
            return False, "UID do e-mail não informado."

        uid_texto = str(email_uid).split(":")[-1]

        print("===== MOVENDO E-MAIL PARA SPAM =====")
        print("EMAIL:", email_usuario)
        print("SERVIDOR:", servidor)
        print("PORTA:", porta)
        print("UID:", uid_texto)
        print("===================================")

        conexao = imaplib.IMAP4_SSL(servidor, porta)
        conexao.login(email_usuario, senha)

        conexao.select("INBOX", readonly=False)

        pastas_spam_possiveis = [
            "[Gmail]/Spam",
            "[Google Mail]/Spam",
            "Spam",
            "Junk",
            "Junk Email"
        ]

        movido = False
        ultima_mensagem = ""

        for pasta_spam in pastas_spam_possiveis:
            status_copy, resposta_copy = conexao.uid(
                "COPY",
                uid_texto,
                pasta_spam
            )

            print("TENTANDO MOVER PARA:", pasta_spam)
            print("STATUS COPY:", status_copy)
            print("RESPOSTA COPY:", resposta_copy)

            if status_copy == "OK":
                conexao.uid("STORE", uid_texto, "+FLAGS", r"(\Deleted)")
                conexao.expunge()
                movido = True
                ultima_mensagem = f"E-mail movido para {pasta_spam}."
                break

        conexao.logout()

        if movido:
            return True, ultima_mensagem

        return False, "Não foi possível encontrar a pasta Spam no IMAP."

    except Exception as erro:
        print("Erro ao mover e-mail para Spam:", erro)
        return False, f"Erro ao mover e-mail para Spam: {erro}"
