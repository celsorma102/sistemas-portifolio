import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime
import pytz

# Configuração do Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configuração do banco de dados de usuários e tarefas
def iniciar_bd_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def iniciar_bd_tarefas():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            descricao TEXT NOT NULL,
            concluida BOOLEAN NOT NULL CHECK (concluida IN (0, 1)),
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_conclusao TIMESTAMP NULL
        )
    """)
    conn.commit()
    conn.close()

# Inicializa os bancos de dados
iniciar_bd_usuarios()
iniciar_bd_tarefas()

# Rotas do Flask
# Página inicial
@app.route("/")
def home():
    if "usuario" in session:
        return render_template("inicial.html", usuario=session["usuario"])
    else:
        return redirect(url_for("login"))
    
# Página de login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        usuario = request.form["username"]
        senha = request.form["password"]

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
        row = cursor.fetchone()
        conn.close()

        if row and check_password_hash(row[0],senha):
            session["usuario"] = usuario
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuário ou senha inválidos!","danger")

    return render_template("login.html")

# Página de registro
@app.route("/registrar", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        usuario = request.form["username"]
        senha = request.form["password"]

        senha_hash = generate_password_hash(senha)

        try:
            conn = sqlite3.connect("usuarios.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, usuario, senha) VALUES (?, ?, ?)", (nome, usuario, senha_hash))
            conn.commit()
            conn.close()
            flash("Registro realizado com sucesso! Faça login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Usuário já existe!", "warning")

    return render_template("registrar.html")

# Página de sistemas
@app.route("/sistemas")
def sistemas():
    if "usuario" not in session:
        flash("Por favor, faça login para acessar os sistemas.", "warning")
        return redirect(url_for("login"))
    else:
        sistemas = [
            {
                "nome": "To-Do List",
                "descricao": "Crie e gerencie suas tarefas diárias de forma simples e eficiente.",
                "link": "/to_do_list"
            }
        ]
        return render_template("sistemas.html",usuario=session["usuario"], sistemas=sistemas)

# Página do To-Do List
@app.route("/to_do_list")
def to_do_list():
    if "usuario" in session:
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarefas WHERE usuario = ?", (session["usuario"],))
        tarefas = cursor.fetchall()
        conn.close()

        # Processar as tarefas para exibição
        tarefas = [list(tarefa) for tarefa in tarefas]

        # Converter os valores de concluído e formatar datas para padrão brasileiro
        if tarefas:
            for tarefa in tarefas:
                concluido = tarefa[3]
                if concluido == 0:
                    tarefa[3] = "Não"
                else:
                    tarefa[3] = "Sim"

                data_str = tarefa[4]
                dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")

                dt_utc = pytz.utc.localize(dt)
                tz_brasilia = pytz.timezone("America/Sao_Paulo")
                dt_brasilia = dt_utc.astimezone(tz_brasilia)
                dt_brasilia_str = dt_brasilia.strftime("%d/%m/%Y %H:%M:%S")
                tarefa[4] = dt_brasilia_str

                data_conclusao = tarefa[5]
                if data_conclusao == None:
                    tarefa[5] = "-"


        return render_template("to_do_list.html", usuario=session["usuario"], tarefas=tarefas)
    else:
        flash("Por favor, faça login para acessar o To-Do List.", "warning")
        return redirect(url_for("login"))

# Adicionar, concluir e deletar tarefas
@app.route("/to_do_list/formulario_add_tarefa", methods=["GET"])
def formulario_add_tarefa():
    if "usuario" in session:
        return render_template("to_do_add.html", usuario=session["usuario"])
    else:
        flash("Por favor, faça login para adicionar tarefas.", "warning")
        return redirect(url_for("login"))

@app.route("/to_do_list/add_tarefa", methods=["POST"])
def add_tarefa():
    if "usuario" in session:
        descricao = request.form["descricao"]
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tarefas (usuario, descricao, concluida) VALUES (?, ?, ?)", (session["usuario"], descricao, False))
        conn.commit()
        conn.close()
        flash("Tarefa adicionada com sucesso!", "success")
        return redirect(url_for("to_do_list"))
    else:
        flash("Por favor, faça login para adicionar tarefas.", "warning")
        return redirect(url_for("login"))

@app.route("/to_do_list/concluir_tarefa/<int:tarefa_id>")
def concluir_tarefa(tarefa_id):
    if "usuario" in session:
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()
        data_conclusao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute("UPDATE tarefas SET concluida = ?, data_conclusao = ? WHERE id = ? AND usuario = ?", (True, data_conclusao, tarefa_id, session["usuario"]))
        conn.commit()
        conn.close()
        flash("Tarefa concluída com sucesso!", "success")
        return redirect(url_for("to_do_list"))
    else:
        flash("Por favor, faça login para concluir tarefas.", "warning")
        return redirect(url_for("login"))
    
@app.route("/to_do_list/deletar_tarefa/<int:tarefa_id>")
def deletar_tarefa(tarefa_id):
    if "usuario" in session:
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ? AND usuario = ?", (tarefa_id, session["usuario"]))
        conn.commit()
        conn.close()
        flash("Tarefa deletada com sucesso!", "success")
        return redirect(url_for("to_do_list"))
    else:
        flash("Por favor, faça login para deletar tarefas.", "warning")
        return redirect(url_for("login"))

# Página de logout
@app.route("/logout")
def logout():
    if "usuario" not in session:
        flash("Você não está logado.", "warning")
        return redirect(url_for("login"))
    else:
        session.pop("usuario", None)
        flash("Logout realizado com sucesso!", "success")
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)