import socket
import openai
import threading

openai.api_key = ""

IP = ''
PORT = 32002
SIZE = 1024
ADDR = (IP, PORT)
clients = []
connection_expire = False

context_pre = 'I made a robot follows a robot language. \
    The robot language is what I made for the robot. I\'ll describe the grammar of the language. \
    D means going forward, B means going backward and RL means rotating left-wise and RR means rotating right-wise. \
    You must add a colon followed by a number, then it describes how much time the robot uses for the left command. \
    The speed of robot is predetermined. It\'s 3cm/s. \
    RL or RR must be also followed by a colon and a number. \
    The number means how much the robot rotates in degrees. \
    I\'ll give you some examples.\nD:13 D:10 RR:5 RL:60 D:1\n\
    The code above means for a robot to go forward for 13 seconds \
    then go forward for 10 seconds then \
    rotate right 5 degrees then rotate left 60 degrees \
    then go forward for 1 second\nPlease translate "'

context_post = '" in the robot language.\nIMPORTANT!!! Do not add any comment! \
    Do not say "To draw something, you can use the following commands". \
    Do not describe nor explain what you provided.'

class Client(threading.Thread):
    
    def __init__(self, clientsocket, address):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.address = address
        self.client_type = 'User'
        print("New connection from %s:%s" % (self.address[0], str(self.address[1])))

    def run(self):
        global clients
        global connection_expire
        print("Connection from : %s" % str(self.address))
        self.client_type = self.clientsocket.recv(1024).decode('utf-8')
        print(self.client_type)
        if self.client_type == 'Robot':
            clients.append(self.clientsocket)
            while not connection_expire:
                pass
        elif self.client_type == 'User':
            while True:
                print(clients)
                data = self.clientsocket.recv(1024)
                msg = data.decode('utf-8')
                if msg == '!!EXIT!!':
                    self.clientsocket.send('!!EXIT!!'.encode())
                    break
                print("Received data from %s:%s : %s" % (self.address[0], str(self.address[1]),msg))
                response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Who are you?"},
                    {"role": "assistant", "content":"I am ChatGPT, a large language model trained by OpenAI. \
                     My purpose is to assist and communicate with users through text-based conversations. \
                     You can ask me questions, seek advice, or just chat about various topics."},
                    {"role": "user", "content": context_pre+msg+context_post}
                    ]
                )
                self.clientsocket.send(response.choices[0].message.content.encode())
                for client in clients:
                    client.send(response.choices[0].message.content.encode())
            # connection_expire = False # 없애기
        if self.client_type == 'Robot':
            clients.remove(clientsocket)
        self.clientsocket.close()
        print("Connection closed %s:%s" % (self.address[0],str(self.address[1])))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(ADDR)
    serversocket.listen()
    print('Listen...')

    while True:
        clientsocket, clientaddr = serversocket.accept()
        newthread = Client(clientsocket,clientaddr)
        newthread.start()
        # clientsocket.sendall(response.choices[0].message.content.encode())

        # clientsocket.close()


