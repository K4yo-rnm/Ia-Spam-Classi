
from backend.services.banco_services import conectar_banco
from services.config_server import carregar_configuracoes


def obter_dashboard():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM emails")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM emails
        WHERE LOWER(classificacao) = 'spam'
    """)
    spam = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM emails
        WHERE LOWER(classificacao) IN (
            'não spam',
            'nao spam',
            'não_spam',
            'nao_spam',
            'ham',
            'normal'
        )
    """)
    nao_spam = total - spam

    cursor.execute("""
        SELECT data_hora FROM emails
        ORDER BY id DESC
        LIMIT 1
    """)
    ultima = cursor.fetchone()

    conexao.close()

    configuracoes = carregar_configuracoes()
    ultima_verificacao = configuracoes.get("ultima_verificacao", "Nenhuma verificação feita")

    return {
        "emails_analisados": total,
        "spam_detectados": spam,
        "nao_spam": nao_spam,
        "ultima_verificacao": ultima_verificacao
    }