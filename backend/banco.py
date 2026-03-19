import sqlite3

conn = sqlite3.connect("backend/banco/banco.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(100),
    online BOOLEAN
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS notificacoes (
    id INTEGER PRIMARY KEY,
    titulo TEXT(500),
    mensagem TEXT(500),
    data DATETIME
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario_notificacoes(
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER,
    notificacao_id INTEGER,
    lida BOOLEAN
)
''')

cursor.execute(
    "SELECT * FROM usuarios")

usuarios = cursor.fetchall()

for usuario in usuarios:
    print(usuario)

conn.commit()
conn.close()