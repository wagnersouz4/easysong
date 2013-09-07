#!/usr/bin/python2.7
#-*- coding:utf-8 -*-

# Framework para a criação de sockets
import SocketServer

# Módulo que permite tocar e gravar audio
import pyaudio

# Módulo que permite a leitura de arquivos wave
import wave

# Módulo que permite utilizar funções do sistema operacional
import os

# Módulo para gerenciamento de log de maneira simples
import logging

# Módulo para manipulação de datas
import datetime

# Conjunto de ferramentas para tornar o trabalho com SQL mais flexível
from sqlalchemy import engine

"""
Módulo que implementa uma inteface comum para diferentes hash de
segurança (md5, sha1, sha512 entre outros)
"""
import hashlib

"""
Classe responsável por gerenciar novas conexões ao servidor.
Usaremos o módulo SocketServer do python que é um framework
para criar servidores de rede.
Seguimos a RFc2616 para retornos de erros - http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
"""

"""
Criando arquivo de log para que irá conter todas as informações sobre o
servidor
"""
logging.basicConfig(filename='mp3facil.log', level=logging.DEBUG)


class ServerRequestsHandler(SocketServer.BaseRequestHandler):

    """
    Instância responsável por gerenciar conexões.
    """

    def handle(self):

        # Escrevendo informações no log
        self.logger = logging.getLogger()
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.logger.info('Server Online - %s', date)

        # Para ter acesso ao sistema o cliente precisa se conectar
        self.auth()
        return

    """
    Instância responsável por gerenciar a autenticação do cliente
    """

    def auth(self):
        """
        Nesse passo iremos enviar (request.send) para o cliente a mensagem de login (User/Password)
        e iremos ler (request.recv) os dados digitos pelo cliente .
        """
        self.request.send('User:')
        self.user = self.request.recv(1024).rstrip('\r\n')
        self.request.send('Password:')
        self.passwd = self.request.recv(1024).rstrip('\r\n')
        self.verify_user()

        try:
            self.connect_db()
        except Exception as e:
            self.server_error(msg_type='database_error', e=e)

        if self.user == 'teste' and self.passwd == 'teste':
            self.request.send('200\n')
            self.verify_user()
            self.logger.info('User %s Conected', self.user)
            self.iteractive()

        else:
            self.request.send('503\n')
            self.logger.info(
                'Login error - User: %s Password: %s', self.user, self.passwd)
            self.request.close()

        return

    """
    Instância responsável por fazer a conexão com o banco de dados
    """

    def connect_db(self):
        #Usaremos o banco de dados mysql
        engine = create_engine(
            'mysql://root:mysqlroot@localhost/sentiment_dict')
        self.connection = engine.connect()

    """
    Instância responsável por verificar a autencidade do usuário
    """

    def verify_user(self):

        # Iremos usar sha512 como algoritmo de segurança hash
        passwd = hashlib.sha512(self.passwd).hexdigest()

        # verificando se usuário está presente no banco
        query = self.connection.execute('select * from negative_pt-br')
        self.result = query.fetchall()
        self.request.send(self.result)

    """
    Instância responsável por gerenciar a iteratividade do servidor
    Neste passo iremos mostrar ao usuário como se interagir com o servidor usando comandos pré-defindos.
    """

    def iteractive(self):

        """
        Atribuindo os comandos a suas funções, list para listar músicas e
        play para tocar uma música em específico
        """
        commands = {
            'list': self.list_files,
            'play': self.play_song
        }

        self.clear_screen()

        self.request.send(
            '------------------COMMANDS AVAILABLE------------------\n')
        self.request.send('list - to list all music files on the server\n')
        self.request.send('play - to enter a filename and than streaming it\n')
        self.request.send('exit - to logout of server\n')
        self.request.send('------------------------------------\n')

        # Lendo a opção digita pelo usuário
        command = self.request.recv(1024).rstrip('\r\n')

        while command != 'exit' and self.verify_request():
            if command not in commands:

                """
                Caso o comando não seja encontrado na lista de comandos
                disponíveis, retornamos 404.
                """
                self.request.send('404\n')
                self.logger.info('Ivalid Command')
            else:
                commands[command]()

            command = self.request.recv(1024).rstrip('\r\n')

        return

    """
    Instância responsável por listar as músicas disponíveis
    """

    def list_files(self):
        self.logger.info('listing files')

        # Listando arquivos disponíveis no diretório de músicas grátis
        try:
            files = os.listdir('./songs/free')
        except Exception as e:
            self.server_error(msg_type='dir_error', e=e)
            return

        for f in files:
            self.request.send(f + '\n')
        self.request.send('\n\n')

        return
    """
    Instância responsável por fazer o streaming de uma música
    """

    def play_song(self):
        self.request.send('Filename:')
        filename = self.request.recv(1024).rstrip('\r\n')

        # Tamanho padrão do chunk - tamanho baseado em exemplos vistos na web
        chunk = 1024

        try:
            s = wave.open('songs/free/' + filename, 'rb')
        except Exception as e:
            self.server_error(msg_type='file_error', e=e)
            return

        self.logger.info('Opened file: %s', filename)

        try:
            data = s.readframes(chunk)
        except Exception as e:
            self.server_error(msg_type='chunk_error', e=e)
            return

        if data:
            self.logger.info('playing a song')

        while data:
            self.request.send(data)

            try:
                data = s.readframes(chunk)
            except Exception as e:
                self.server_error(msg_type='chunk_error', e=e)
                return

        self.logger.info('end playing a song')
        self.request.send('Song end')
        self.clear_screen()
        self.iteractive()

    """
    Instância responsável pelo gerenciamento de erros no servidor
    """

    def server_error(self, msg_type, e):
        # Tipos de mensagem de erro
        msg = {'chunk_error': 'Error while processing file', 'file_error':
               'Invalid filename', 'dir_error': 'Server listing error', 'database_error': 'Server database error'}

        self.logger.info('Exception Occurred : %s', e)
        self.request.send(msg[msg_type] + ' - Try again :-)\n')

    """
    Instância responsável por simular uma limpeza de tela
    """

    def clear_screen(self):
        for i in xrange(0, 10):
            self.request.send('\n')

if __name__ == '__main__':

    import threading

    """
    Aqui definimos a tupla (endereço, porta) do servidor.
    Neste caso usarmos a porta 8888. Não há um motivo especial
    para a escolha dessa porta.
    Também é possível deixar que o kernel selecione uma porta automaticamente,
    para isso deve-se usar o valor 0.
    Usaremos o endereço 0.0.0.0 que nada mais é do que o ip atual da máquina.
    """
    server_address = ('0.0.0.0', 8888)

    """
    Subindo um servidor do tipo TCP, usando o endereço do servidor
    e a classe que irá gerenciar o mesmo.
    """
    server = SocketServer.TCPServer(server_address, ServerRequestsHandler)

    t = threading.Thread(target=server.serve_forever)
    # t.setDaemon(True)  # don't hang on exit
    t.start()

"""
Neste ponto, criamos um servidor socket usando IPv4 = AF_INET, é possível usar
IPv6 com AF_INET6. Definimos também qual o tipo do protocolo de transporte,
neste caso usarmos TCP = SOCK_STREAM.
"""


"""
            print ('Conectado. :-) \n')

"""
