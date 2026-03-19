import sqlite3

conn = sqlite3.connect("backend/banco/banco.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO usuarios (nome, email, senha, online) VALUES (?, ?, ?, ?)",
    ("Eduardo2", "eduardo@teste2.com", "senhateste2", True)
    )

conn.commit()
conn.close()