import socket

SERVER_IP = '0.0.0.0' # SERVER IP
SERVER_PORT = 0 #SERVER PORT
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
    clientsocket.connect(SERVER_ADDR)
    clientsocket.send('User'.encode())
    while True:
        query = input('> ')
        clientsocket.send(query.encode())
        msg = clientsocket.recv(SIZE).decode('utf-8')
        if msg == '!!EXIT!!':
            break
        print(msg)
    clientsocket.close()
