
import sys
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from services.banco_services import preparar_banco

import os

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ_PROJETO))

from backend.routes import registrar_rotas

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)
app.secret_key = "chave-dev-ia-spam-classifier"
CORS(app)

preparar_banco()
registrar_rotas(app)


if __name__ == "__main__":
    app.run(debug=True)