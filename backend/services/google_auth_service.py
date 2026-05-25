
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAMINHO_CREDENTIALS = os.path.join(BASE_DIR, "credentials.json")
CAMINHO_TOKEN = os.path.join(BASE_DIR, "token_google.json")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


def criar_fluxo_google():
    flow = Flow.from_client_secrets_file(
        CAMINHO_CREDENTIALS,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:5000/callback-google"
    )

    return flow


def salvar_credenciais_google(credentials):
    dados_token = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }

    with open(CAMINHO_TOKEN, "w", encoding="utf-8") as arquivo:
        json.dump(dados_token, arquivo, indent=4, ensure_ascii=False)


def carregar_credenciais_google():
    if not os.path.exists(CAMINHO_TOKEN):
        return None

    credentials = Credentials.from_authorized_user_file(
        CAMINHO_TOKEN,
        SCOPES
    )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        salvar_credenciais_google(credentials)

    return credentials


def google_esta_conectado():
    credentials = carregar_credenciais_google()

    if not credentials:
        return False

    return credentials.valid or bool(credentials.refresh_token)


def desconectar_google():
    if os.path.exists(CAMINHO_TOKEN):
        os.remove(CAMINHO_TOKEN)

    return True