from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect("backend/banco/banco.db", check_same_thread=False)
cursor = conn.cursor()

@app.route("/cadastro", methods = ["POST"])
def cadastro():
    dados = request.json

    nome = dados ["nome"]
    email = dados ["email"]
    senha = dados ["senha"]

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? OR nome = ?",
        (email, nome)
    )
    
    usuario = cursor.fetchone()

    if nome and email and senha and not usuario:
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, online) VALUES(?, ?, ?, ?)",
                (nome, email, senha, False)
            )

            usuario_id = cursor.lastrowid

            conn.commit()

            return jsonify({
                "sucesso": "Conta criada com sucesso",
                "id": usuario_id}), 201
        
        except Exception as erro:
            return jsonify ({"erro": "Erro inesperado"}), 500
    elif usuario:
        return jsonify ({"erro": "usuário já existe"}), 409
    
@app.route("/login", methods = ["POST"])
def login():
    dados = request.json

    nome = dados["nome"]
    senha = dados ["senha"]

    cursor.execute(
        "SELECT id, senha FROM usuarios WHERE nome = ?",
        (nome,)
    )

    usuario = cursor.fetchone()

    if not usuario:
        return jsonify({"erro": "usuário não encontrado"}), 404
    
    usuario_id = usuario[0]
    senha_db = usuario[1]

    if senha != senha_db:
        return jsonify({"erro": "senha incorreta"}), 401
    elif senha == senha_db:
        return jsonify({
            "sucesso": "login realizado",
            "id": usuario_id}), 200
    
@app.route("/enviar_notificacao", methods = ["POST"])
def enviar_notificacao():
    dados = request.json

    titulo = dados["titulo"]
    mensagem = dados["mensagem"]
    usuarios = dados["usuarios"]

    cursor.execute(
        "INSERT INTO notificacoes (titulo, mensagem) VALUES(?, ?)",
        (titulo, mensagem)
        )
    
    notificacao_id = cursor.lastrowid

    for usuario_id in usuarios:
        cursor.execute(""
        "INSERT INTO usuario_notificacoes (usuario_id, notificacao_id, lida) VALUES(?, ?, ?)",
        (usuario_id, notificacao_id, False))

    conn.commit()

    return jsonify({"sucesso": "notificação enviada"})

@app.route("/notificacoes/<int:usuario_id>")
def notificacoes(usuario_id):

    cursor.execute("""
    SELECT notificacoes.titulo, notificacoes.mensagem
    FROM notificacoes
    JOIN usuario_notificacoes
    ON notificacoes.id = usuario_notificacoes.notificacao_id
    WHERE usuario_notificacoes.usuario_id = ?
    """, (usuario_id,))

    dados = cursor.fetchall()

    resultado = []

    for titulo, mensagem in dados:
        resultado.append({
        "titulo": titulo,
        "mensagem": mensagem
    })

    return jsonify(resultado)

@app.route("/notificacao/lida", methods=["POST"])
def marcar_como_lida():
    dados = request.json

    usuario_id = dados["usuario_id"]
    notificacao_id = dados["notificacao_id"]

    cursor.execute(
        "UPDATE usuario_notificacoes SET lida = ? WHERE usuario_id = ? AND notificacao_id = ?",
        (True, usuario_id, notificacao_id)
    )

    conn.commit()

    return jsonify({"sucesso": "Notificação marcada como lida"})

@app.route("/notificacoes/nao_lidas/<int:usuario_id>")
def nao_lidas(usuario_id):

    cursor.execute("""
    SELECT COUNT(*)
    FROM usuario_notificacoes
    WHERE usuario_id = ? AND lida = 0
    """, (usuario_id,))

    total = cursor.fetchone()[0]

    return jsonify({"nao_lidas": total})

@app.route("/admin_painel")
def painel():

    cursor.execute(
        "SELECT id, nome FROM usuarios")
    
    usuario = cursor.fetchall()

    usuarios = []

    for usuario_id, usuario_nome in usuario:
        usuarios.append({
            "id":usuario_id,
            "nome":usuario_nome
        })

    return jsonify(usuarios)
        
if __name__ == "__main__":
    app.run(debug=True)