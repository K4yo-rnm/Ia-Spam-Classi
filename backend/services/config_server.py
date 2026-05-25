import json
from pathlib import Path


RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
CAMINHO_CONFIG = RAIZ_PROJETO / "database" / "configuracoes.json"


CONFIG_PADRAO = {
    "intervalo": "5",
    "analisar_nao_lidos": True,
    "mover_spam": False,
    "notificacoes": True,
    "notificacao_area": True,
    "idioma": "pt-BR",
    "tema": "claro",
    "ultima_verificacao": "Nenhum verificação feita"
}


def carregar_configuracoes():
    if not CAMINHO_CONFIG.exists():
        salvar_configuracoes(CONFIG_PADRAO)
        return CONFIG_PADRAO

    with open(CAMINHO_CONFIG, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_configuracoes(configuracoes):
    CAMINHO_CONFIG.parent.mkdir(parents=True, exist_ok=True)

    with open(CAMINHO_CONFIG, "w", encoding="utf-8") as arquivo:
        json.dump(configuracoes, arquivo, indent=4, ensure_ascii=False)

    return configuracoes