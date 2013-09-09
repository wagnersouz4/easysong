#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

# importando funcionalidades do frameworok flask
try:
    from flask import Flask, request, session, redirect, url_for, render_template, flash
except ImportError:
    raise ImportError(
        "The flask framework is required to run this program. Run `pip install flask`")

from client import StreamingClientSocket

# Criando uma nova aplicação
app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='666',
))

# Criando do socket da aplicação
app.socket = StreamingClientSocket(ip='0.0.0.0', port=8888)

# Página principal
@app.route('/')
def list_songs():
	songs = []

	if app.socket.is_connected() and session['logged_in']:
		songs = app.socket.list_songs()

	return render_template('list_songs.html', songs=songs)

@app.route('/play/<song>', methods=['GET'])
def play(song):	
	app.socket.stream_song(song=song)
	return redirect(url_for('list_songs'))

@app.route('/buy/<song>', methods=['GET'])
def buy(song):
	result = app.socket.buy_song(song=song)
	if result == 200:
		msg = song+' comprado. Verifique sua pasta de download!'
		session['money'] = app.socket.get_money()
	else:
		msg = 'Saldo insuficiente'

	flash(msg.decode('utf8'))
	return redirect(url_for('list_songs'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	user = request.form['username']
    	passwd = request.form['passwd']
    	app.socket.connect_socket(user=user, passwd=passwd)
    	if not app.socket.is_connected():
    		session['logged_in'] = False
    		error='Dados incorretos'

    	else:
    		session['logged_in'] = True
    		session['user'] = user
    		session['money'] = app.socket.get_money()
    		flash('Autenticado no sistema')
    		return redirect(url_for('list_songs'))
    	
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    app.socket = StreamingClientSocket(ip='0.0.0.0', port=8888)
    flash('Desconectado do sistema')
    return redirect(url_for('list_songs'))


if __name__ == '__main__':
    app.run('0.0.0.0')
