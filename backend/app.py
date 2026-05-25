
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_cors import CORS

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ_PROJETO))

CAMINHO_ENV = RAIZ_PROJETO / ".env"
load_dotenv(CAMINHO_ENV)

from services.banco_services import preparar_banco
from backend.routes import registrar_rotas

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = os.getenv(
    "OAUTHLIB_INSECURE_TRANSPORT",
    "0"
)

FRONTEND_DIR = RAIZ_PROJETO / "frontend"

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)

app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY não encontrada. Configure SECRET_KEY no .env ou nas variáveis do Render.")

CORS(app)

@app.route("/")
def pagina_inicial():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:arquivo>")
def servir_frontend(arquivo):
    return send_from_directory(FRONTEND_DIR, arquivo)

preparar_banco()
registrar_rotas(app)

if __name__ == "__main__":
    app.run(debug=True)