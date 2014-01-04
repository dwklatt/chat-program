import sys, socket
from thread import *

#will add a way to define host and port
HOST = ''
PORT = 8888
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST,PORT))
client.sendall('testing')
while 1:
#	client.sendall('testing')
	msg = client.recv(1024)
	print msg

