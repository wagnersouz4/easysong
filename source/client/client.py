#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import socket
import pyaudio
import cPickle as pickle

"""
Está classe irá gerentciar as conexões com o servidor socket
"""


class StreamingClientSocket(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    """
    Instância responsável por fazer a conexão com o servidor <socket></socket>
    """

    def connect_socket(self, user, passwd):
        """
        Neste ponto usaremos um socket com IPv4 = AF_INET, é possível usar
        IPv6 com AF_INET6. Definimos também qual o tipo do protocolo de transporte,
        neste caso usarmos TCP = SOCK_STREAM.
        """
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cli.connect((self.ip, self.port))
        self.user = user
        self.passwd = passwd

        if self.verify_user():
            self.connected = True
        else:
            self.connected = False

    """
    Instância responsável por listar múscias
    """

    def list_songs(self):
        # enviando o comando para listar múscias
        if self.is_connected:
            self.cli.send('list')
            songs = pickle.loads(self.cli.recv(1024))
            if songs:
                return songs
            else:
                return []
        else:
            return 403

    """
    Instância responsável por fazer o streamming de uma música
    """

    def stream_song(self, song):
        if self.is_connected():
            self.cli.send('play')
            self.cli.recv(1024)
            self.cli.send(song)
            data = self.cli.recv(1024)

            if 'error' not in data:

                p = pyaudio.PyAudio()

                stream = p.open(
                    format=p.get_format_from_width(pyaudio.paInt32),
                    channels=2,
                    rate=44100,
                    frames_per_buffer=1024,
                    output=True
                )

                while 'end' not in data:
                    stream.write(data)
                    data = self.cli.recv(1024)

                # fechando o streaming
                stream.stop_stream()
                stream.close()
                p.terminate()
        else:
            return 403

    def buy_song(self, song):

        if self.is_connected:
            self.cli.send('buy')
            self.cli.recv(1024)
            self.cli.send(song)

            data = self.cli.recv(1024)

            if '404' in data:
                return 404

            elif '403' in data:
                return 403

            else:
                # Criando o arquivo com a música
                song = open(song + '.mp3', 'wb')
                while 'end' not in data:
                    song.write(data)
                    data = self.cli.recv(1024)
        else:
            return 403




    """
    Instância por retornar o status da conexão
    """
    def is_connected(self):
        return self.connected

    """
    Instância responsável por verificar a autenticidade do usuário
    """
    def verify_user(self):
        """
        Neste ponto iremos receber os outputs do servidor e enviaremos inputs
        """
        self.cli.recv(1024)
        self.cli.send(self.user)
        self.cli.recv(1024)
        self.cli.send(self.passwd)

        result = self.cli.recv(1024)

        """
        Recebendo menu de opções, que não será usado nessa cliente, mas é válido quando
        usa-se telnet para se conectar no servidor
        """
        self.cli.recv(1024)

        if not result == '503':
            return True

        else:
            return False

s = StreamingClientSocket(ip='0.0.0.0', port=8888)
s.connect_socket(user='andre', passwd='andre')
s.list_songs()
s.buy_song(song='Back In Black')

"""
# se o usuario for invalido ele volta 503
# caso contrário ele volta 200+lista do comandos


# recebe resposta se autenticou ou não
clisock.recv(1024)


# enviando o comando play preciso de um recv logo após, pois precisamos
# digitar o filename
clisock.send('play')

# recebe o filename
clisock.recv(1024)

# envia o filename
clisock.send('Back In Black')

# em caso de achar usar esse processo para tocar a musica
data = clisock.recv(1024)

p = pyaudio.PyAudio()

stream = p.open(
    format=p.get_format_from_width(pyaudio.paInt32),
    channels=2,
    rate=44100,
    output=True
)

while data != 'Song end':
    # print data
    stream.write(data)
    data = clisock.recv(1024)
    print data

# stream.close()
# p.terminate()
"""
