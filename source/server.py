#!/usr/bin/python2.7
#-*- coding:utf-8 -*-

import SocketServer
import pyaudio
import wave
import os

"""
Classe responsável por gerenciar novas conexões ao servidor.
Usaremos o módulo SocketServer server do python que é um framework
para criar servidores de rede.
"""


class ServerRequestsHandler(SocketServer.BaseRequestHandler):

    """
    Instância responsável por gerenciar conexões
    """

    def handle(self):
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
        user = self.request.recv(1024).rstrip('\r\n')
        self.request.send('Password:')
        passwd = self.request.recv(1024).rstrip('\r\n')

        print (user, passwd)

        if user == 'teste' and passwd == 'teste':
            self.iteractive()

        else:
            self.request.send('Ivalid User\n')
            self.request.close()

        return

    """
    Instância responsável por gerenciar a iteratividade do servidor
    """

    def iteractive(self):
        """
        Neste passo iremos mostrar ao usuário como se interagir com o servidor usando
        comando pré-defindos.
        """
        commands = {
            'list': self.list_files,
            'play': self.play_song
        }

        self.clear_screen()

        self.request.send('------------------------------------\n')
        self.request.send('Logged user\n')
        self.request.send('Use the commands below:\n')
        self.request.send('list - to list all music files on the server\n')
        self.request.send('play - to enter a filename and than streaming it\n')
        self.request.send('exit - to logout of server\n')
        self.request.send('------------------------------------\n')

        # Lendo a opção digita pelo usuário
        command = self.request.recv(1024).rstrip('\r\n')

        while command != 'exit':
            if command not in commands:
                self.request.send('Ivalid Command\n')
            else:
                commands[command]()

            command = self.request.recv(1024).rstrip('\r\n')

        return

    def list_files(self):
        print ('listing files')
        files = os.listdir('./songs/free')        
        for f in files:
            self.request.send(f+'\n')
        self.request.send('\n\n')

        return

    def play_song(self):
        print ('playing a song')
        self.request.send('Filename:')
        filename = self.request.recv(1024).rstrip('\r\n')

        chunk = 1024
        s = wave.open('songs/free/'+filename,'rb')
        data = s.readframes(chunk)

        while data != '':
            #stream.write(data)
            self.request.send(data)
            data = s.readframes(chunk)

        self.request.send('end')
        print 'streamming end'

        return

    def clear_screen(self):
        for i in xrange(0, 10):
            self.request.send('\n')

if __name__ == '__main__':

    #import threading

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
    server.serve_forever()

    
    #t = threading.Thread(target=server.serve_forever)
    #t.setDaemon(True)  # don't hang on exit
    #t.start()
    


"""
Neste ponto, criamos um servidor socket usando IPv4 = AF_INET, é possível usar
IPv6 com AF_INET6. Definimos também qual o tipo do protocolo de transporte,
neste caso usarmos TCP = SOCK_STREAM.
"""


"""
            print ('Conectado. :-) \n')

"""
