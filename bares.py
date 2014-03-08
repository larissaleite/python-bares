#! /usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, os
from flask import Flask, render_template, request, g, redirect, url_for

app = Flask (__name__)
app.debug = True

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

""" Lista todos os bares cadastrados """
@app.route("/listaBares", methods=["GET", "POST"])
def listaBares():
	db = get_db()
	cur = db.execute('select * from bares')
	bares = cur.fetchall()
	return render_template('listaBares.html', bares=bares)

""" Exibe na pagina editarBar.thml o bar referente ao id passado como parametro """
@app.route("/editarBar/<bar_id>", methods=["GET", "POST"])
def editarBar(bar_id):
	db = get_db()
	cur = db.execute("select * from bares where id = '%s';" %bar_id)
	bares = cur.fetchall()
	return render_template('editarBar.html', bares=bares)

""" Remove o bar do banco de dados """
@app.route("/removerBar/<bar_id>")
def removerBar(bar_id):
	db = get_db()
	db.execute("delete from bares where id = '%s';" %bar_id)
	db.commit()
	return redirect(url_for('listaBares'))

""" Atualiza o bar com os novos atributos """
@app.route("/atualizarBar/<bar_id>", methods=["GET", "POST"])
def atualizarBar(bar_id):
	if request.method == "POST":
		nome = request.form.get("nome")
		descricao = request.form.get("desc")
		imagem = request.form.get("img")
		endereco = request.form.get("end")
		telefone = request.form.get("tel")
		especialidade = request.form.get("especialidade")

	db = get_db()
	db.execute("update bares set nome=?, descricao=?, imagem=?, endereco=?, telefone=?, especialidade=? where id=?", (nome, descricao, imagem, endereco, telefone, especialidade, bar_id))
	db.commit()
	return redirect(url_for('listaBares'))

""" Cadastra o bar com os dados do formulário """
@app.route("/bar", methods=["GET", "POST"])
def bar():
	if request.method == "POST":
		nome = request.form.get("nome")
		descricao = request.form.get("desc")
		imagem = request.form.get("img")
		endereco = request.form.get("end")
		telefone = request.form.get("tel")
		especialidade = request.form.get("especialidade")

	"""return "Bar %s %s %s %s" % (nome, endereco, horario, especialidade)"""
	db = get_db()
	db.execute('insert into bares (nome, descricao, imagem, endereco, telefone, especialidade) values (?, ?, ?, ?, ?, ?)',[nome, descricao, imagem, endereco, telefone, especialidade])
	db.commit()
	return redirect(url_for('listaBares'))

@app.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
    app.run() #herda de flask, levanta o servidor
    init_db()