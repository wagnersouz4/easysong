import socket
import pyaudio
"""
class StreamingClientSocket(object):

	def __init__(self, sever_address, username, passwd):
		self.server_address = server_address
		self.connect()

	def create_socket(self):
		self.clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self, username, passwd):
		self.clisock.connect(self.server_address)
		self.clisock.send(username)
		self.clisock.recv(1024)
		self.clisock.send(passwd)

		status = self.clisock.recv(1024)

		if status == 'Logged':
			print 'opa loguei'

		else:
			self.clisock.dis

"""
clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ('0.0.0.0',8888)

clisock.connect(address)

#login
clisock.send('teste')
clisock.recv(1024)
clisock.send('teste')

#limpa tela
clisock.recv(1024)

#mostra menu
clisock.recv(1024)

#commando play
clisock.send('play')

#recebe o Filename:
clisock.recv(1024)

#envia nome do arquivo
clisock.send('acdc2.wav')

data = clisock.recv(1024)

p = pyaudio.PyAudio()

stream = p.open(
        format = p.get_format_from_width(pyaudio.paInt32),
        channels = 2,
        rate = 44100,
        output = True
    )

while data != 'end':
	stream.write(data)
	data = clisock.recv(1024)

stream.close()
p.terminate()

