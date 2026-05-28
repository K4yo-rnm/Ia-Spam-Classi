
import sqlite3
from datetime import datetime
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
CAMINHO_BANCO = RAIZ_PROJETO / "database" / "banco.db"

def conectar_banco():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """
    return sqlite3.connect(CAMINHO_BANCO)

def salvar_email(remetente, assunto, conteudo, classificacao, email_uid=None, data_hora=None):
    """
    Salva um e-mail analisado no banco de dados.
    Se email_uid for informado, evita salvar duplicado.
    """

    if email_uid and email_ja_existe(email_uid):
        return False

    conexao = conectar_banco()
    cursor = conexao.cursor()

    if not data_hora:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
        INSERT INTO emails (remetente, assunto, conteudo, classificacao, data_hora, email_uid)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (remetente, assunto, conteudo, classificacao, data_hora, email_uid))

    conexao.commit()
    conexao.close()

    return True
   
def listar_utlimos_emails(limite=10):
        try:
            limite = int(limite)

            conexao = conectar_banco()
            cursor = conexao.cursor()

            print("Limite:", limite)
            print("Tipo do limite:", type(limite))

            cursor.execute("""
                SELECT remetente, assunto, classificacao, data_hora
                FROM emails
                ORDER BY id DESC
                LIMIT ?
            """, (limite,))

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

            return emails

        except Exception as error:
            print("Erro na rota /emails:", error)

            return {
                "status": "erro",
                "erro": "Erro ao listar e-mails",
                "detalhe": str(error)
            }, 400
        
def preparar_banco():
    """
    Garante que a tabela emails tenha a coluna email_uid
    e cria um índice único para evitar duplicidade.
    """

    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        cursor.execute("ALTER TABLE emails ADD COLUMN email_uid TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_emails_uid
        ON emails(email_uid)
    """)

    conexao.commit()
    conexao.close()

def email_ja_existe(email_uid):
    """
    Verifica se um e-mail já foi salvo no banco pelo UID.
    """

    if not email_uid:
        return False

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id FROM emails
        WHERE email_uid = ?
        LIMIT 1
    """, (email_uid,))

    resultado = cursor.fetchone()

    conexao.close()

    return resultado is not None
