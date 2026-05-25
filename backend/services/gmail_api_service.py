import base64
from datetime import datetime
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build

from services.google_auth_service import carregar_credenciais_google


def criar_servico_gmail():
    credentials = carregar_credenciais_google()

    if not credentials:
        return None

    return build("gmail", "v1", credentials=credentials)


def pegar_header(headers, nome):
    for header in headers:
        if header.get("name", "").lower() == nome.lower():
            return header.get("value", "")

    return ""


def formatar_data_email_google(data_email):
    if not data_email:
        return datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        data_convertida = parsedate_to_datetime(data_email)

        if data_convertida.tzinfo is None:
            data_convertida = data_convertida.replace(tzinfo=ZoneInfo("UTC"))

        data_brasil = data_convertida.astimezone(ZoneInfo("America/Sao_Paulo"))

        return data_brasil.strftime("%d/%m/%Y %H:%M")

    except Exception as erro:
        print("Erro ao formatar data Gmail API:", erro)
        return data_email


def extrair_texto_payload(payload):
    corpo = ""

    if "parts" in payload:
        for parte in payload["parts"]:
            mime_type = parte.get("mimeType", "")

            if mime_type == "text/plain":
                data = parte.get("body", {}).get("data")

                if data:
                    texto_bytes = base64.urlsafe_b64decode(data)
                    corpo += texto_bytes.decode("utf-8", errors="ignore")

            elif "parts" in parte:
                corpo += extrair_texto_payload(parte)

    else:
        data = payload.get("body", {}).get("data")

        if data:
            texto_bytes = base64.urlsafe_b64decode(data)
            corpo += texto_bytes.decode("utf-8", errors="ignore")

    return corpo.strip()


def buscar_ultimos_emails_gmail_api(limite=10, apenas_nao_lidos=True):
    try:
        service = criar_servico_gmail()

        if not service:
            return False, "Google não está conectado.", []

        query = "in:inbox"

        if apenas_nao_lidos:
            query += " is:unread"

        resultado = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=int(limite)
        ).execute()

        mensagens = resultado.get("messages", [])

        emails = []

        for item in mensagens:
            message_id = item.get("id")

            mensagem = service.users().messages().get(
                userId="me",
                id=message_id,
                format="full"
            ).execute()

            payload = mensagem.get("payload", {})
            headers = payload.get("headers", [])

            remetente = pegar_header(headers, "From")
            assunto = pegar_header(headers, "Subject")
            data_original = pegar_header(headers, "Date")
            data_formatada = formatar_data_email_google(data_original)
            conteudo = extrair_texto_payload(payload)

            emails.append({
                "email_uid": f"gmail_api:{message_id}",
                "gmail_message_id": message_id,
                "remetente": remetente,
                "assunto": assunto,
                "data": data_formatada,
                "data_original": data_original,
                "conteudo": conteudo[:1000]
            })

        return True, "E-mails buscados com sucesso pela Gmail API.", emails

    except Exception as erro:
        print("Erro ao buscar e-mails pela Gmail API:", erro)
        return False, f"Erro ao buscar e-mails pela Gmail API: {erro}", []


def mover_email_para_spam_gmail_api(message_id):
    try:
        service = criar_servico_gmail()

        if not service:
            return False, "Google não está conectado."

        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={
                "addLabelIds": ["SPAM"],
                "removeLabelIds": ["INBOX"]
            }
        ).execute()

        return True, "E-mail movido para Spam pela Gmail API."

    except Exception as erro:
        print("Erro ao mover e-mail para Spam pela Gmail API:", erro)
        return False, f"Erro ao mover e-mail para Spam pela Gmail API: {erro}"