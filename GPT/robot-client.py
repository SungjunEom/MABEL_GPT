import socket
import time
import serial

SERVER_IP = '0.0.0.0' # SERVER IP
SERVER_PORT = 0 # SERVER PORT
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

ser = serial.Serial('/dev/ttyACM0',baudrate=9600)
time.sleep(1)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        try:
            clientsocket.connect(SERVER_ADDR)
            clientsocket.send('Robot'.encode())
            ser.write('0'.encode())
            while True:
                msg = clientsocket.recv(SIZE).decode('utf-8')
                if msg == '!!EXIT!!':
                    break
                print(msg)

                # parsing
                msg = msg.split(' ')
                for command in msg:
                    command = command.split(':')
                    if command[0] == 'D':
                        for i in range(0,int(command[1])):
                            ser.write('4'.encode())
                            time.sleep(1)
                    elif command[0] == 'RL':
                        for i in range(0, int(command[1])):
                            ser.write('1'.encode())
                            time.sleep(1)
                    elif command[0] == 'RR':
                        for i in range(0, int(command[1])):
                            ser.write('2'.encode())
                            time.sleep(1)
                    elif command[0] == 'B':
                        for i in range(0, int(command[1])):
                            ser.write('8'.encode())
                            time.sleep(1)
                ser.write('0'.encode())
            clientsocket.close()
        except:
            pass
    time.sleep(10)
