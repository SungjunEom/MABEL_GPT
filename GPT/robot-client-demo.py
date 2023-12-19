import socket
import time
import serial

SERVER_IP = '0.0.0.0' # SERVER IP
SERVER_PORT = 0 # SERVER PORT
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

#ser = serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=1)
#ser.reset_input_buffer()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        try:
            clientsocket.connect(SERVER_ADDR)
            clientsocket.send('Robot'.encode())
            #ser.write(b'0')
            print(0,end='')
            while True:
                msg = clientsocket.recv(SIZE).decode('utf-8')
                if msg == '!!EXIT!!':
                    break
                #print(msg)

                # parsing
                msg = msg.split(' ')
                print(msg)
                for command in msg:
                    command = command.split(':')
                    if command[0] == 'D':
                        for i in range(0,int(command[1])):
                            #ser.write(b'4')
                            print(4,end='', flush=True)
                            time.sleep(0.1)
                    elif command[0] == 'RL':
                        for i in range(0, int(int(command[1])/10)):
                            #ser.write(b'1')
                            print(1,end='', flush=True)
                            time.sleep(0.1)
                    elif command[0] == 'RR':
                        for i in range(0, int(int(command[1])/10)):
                            #ser.write(b'2')
                            print(2,end='', flush=True)
                            time.sleep(0.1)
                    elif command[0] == 'B':
                        for i in range(0, int(command[1])):
                            #ser.write(b'8')
                            print(8,end='', flush=True)
                            time.sleep(0.1)
                #ser.write(b'0')
                print(0)
            clientsocket.close()
            break
        except:
            pass
    time.sleep(10)
