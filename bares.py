#! /usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, render_template, request, g

app = Flask (__name__)
app.debug = True

@app.route("/bar", methods=["GET", "POST"])
def bar():
	if request.method == "POST":
		nome = request.form.get("nome")
		endereco = request.form.get("end")
		horario = request.form.get("horario")
		especialidade = request.form.get("especialidade")

	return "Bar %s %s %s %s" % (nome, endereco, horario, especialidade)

@app.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
    app.run() #herda de flask, levanta o servidor