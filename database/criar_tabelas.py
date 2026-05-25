import sqlite3

conexao = sqlite3.connect("database/banco.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remetente TEXT NOT NULL,
    assunto TEXT NOT NULL,
    conteudo TEXT,
    classificacao TEXT NOT NULL,
    data_hora TEXT NOT NULL
)
""")

conexao.commit()
conexao.close()

print("Tabela emails criada com sucesso!")