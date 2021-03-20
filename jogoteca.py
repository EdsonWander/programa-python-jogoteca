from flask import Flask, render_template, request, redirect, session, flash, url_for
from jogo import Jogo
from usuario import Usuario

app = Flask(__name__)
app.secret_key = 'edson'

jogo1 = Jogo("Super Mario", "Plataforma", "Super Nintendo")
jogo2 = Jogo("Pokémon Gold", "RPG", "Game Boy")
jogo3 = Jogo("Mortal Kombat", "Luta", "Super Nintendo")
jogo4 = Jogo("Doom", "Tiro", "Super Nintendo")

lista = [jogo1, jogo2, jogo3, jogo4]

usuario1 = Usuario('edson', 'Edson Wander', '123456')
usuario2 = Usuario('jose', 'Jose Jacinto', '654321')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2}

@app.route('/')
def index():
    return render_template("lista.html", titulo="Jogos", jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template("novo.html", titulo="Novo Jogo")

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)

    lista.append(jogo)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():

    if request.form['usuario'] in usuarios:
        user = usuarios[request.form['usuario']]
        if user.senha == request.form['senha']:
            session['usuario_logado'] = user.id
            flash(user.id + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Não logado, tente novamente!')
            return redirect(url_for('login'))
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuario logado!')
    return redirect(url_for('index'))

app.run(debug=True)