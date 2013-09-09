#!/usr/bin/env python2.7
# -*- coding: utf8 -*-


import socket

try:
    import pyaudio
except ImportError:
    raise ImportError(
        "The pyaudio module is required to run this program. Run `pip install pyaudio`")

import cPickle as pickle

"""
Está classe irá gerentciar as conexões com o servidor socket
"""


class StreamingClientSocket(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connected = False
    """
    Método responsável por fazer a conexão com o servidor <socket></socket>
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
            self.cli.close()

    """
    Método responsável por fazer a desconexão com o servidor
    """
    def socket_disconnect(self):
        self.cli.close()

    """
    Método responsável por listar múscias
    """

    def list_songs(self):
        # enviando o comando para listar múscias
        if self.is_connected():
            self.cli.send('list')
            songs = pickle.loads(self.cli.recv(1024))
            if songs:
                return songs
            else:
                return []
        else:
            return 403

    """
    Método responsável por fazer o streamming de uma música
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

        if self.is_connected():
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
                song = open('downloads/' + song + '.mp3', 'wb')

                while '0x1A' not in data:
                    song.write(data)
                    data = self.cli.recv(1024)

                return 200
        else:
            return 403

    """
    Método responsável por retornar o status da conexão
    """

    def is_connected(self):
        return self.connected

    """
    Método responsável por retornar o saldo do usuário
    """

    def get_money(self):
        if self.is_connected():
            self.cli.send('money')
            return self.cli.recv(1024).strip('\r\n')
        else:
            return 403

    """
    Método responsável por verificar a autenticidade do usuário
    """

    def verify_user(self):
        """
        Neste ponto iremos receber os outputs do servidor e enviaremos inputs
        """
        print self.user, self.passwd
        self.cli.recv(1024)
        self.cli.send(self.user)
        self.cli.recv(1024)
        self.cli.send(self.passwd)

        result = self.cli.recv(1024).rstrip('\r\n')
        print result

        """
        Recebendo menu de opções, que não será usado nessa cliente, mas é válido quando
        usa-se telnet para se conectar no servidor
        """
        self.cli.recv(1024)

        if result == '200':
            return True

        else:
            return False

if __name__ == '__main__':
    s = StreamingClientSocket(ip='0.0.0.0', port=8888)
    s.connect_socket(user='andre', passwd='andre')
    s.list_songs()
    s.get_money()
    s.stream_song(song='Thunderstruck')
