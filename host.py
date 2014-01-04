import socket, sys
from thread import *

#will add a way to define host and port
HOST = ''
PORT = 8888

#socket setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
try:
    server.bind((HOST,PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'server created'

server.listen(10)

print 'now listening'

#creates a thread for each connection
#will act as the chatroom
def room(conn):
    print('new particapant!')
    conn.sendall('Welcome to the server')
    while True:
        
        data = conn.recv(1024)
        if not data:
            break
        for participants in connections:
            participants.sendall(data)
        conn.sendall(data)

    conn.close()

#keeps the server going
while 1:
    conn, addr = server.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    connections.append(conn)
    start_new_thread(room, (conn,))

server.close()

