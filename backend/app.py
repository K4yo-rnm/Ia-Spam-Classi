import sys
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from services.banco_services import preparar_banco


RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ_PROJETO))

from backend.routes import registrar_rotas


app = Flask(__name__)
CORS(app)

preparar_banco()
registrar_rotas(app)


if __name__ == "__main__":
    app.run(debug=True)