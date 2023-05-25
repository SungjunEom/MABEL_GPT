import socket
import time
import serial

SERVER_IP = '3.26.71.117'
SERVER_PORT = 32002
SIZE = 1024
SERVER_ADDR = (SERVER_IP, SERVER_PORT)

ser = serial.Serial('/dev/ttyACM0',9600,timeout=1)
ser.reset_input_buffer()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        try:
            clientsocket.connect(SERVER_ADDR)
            clientsocket.send('Robot'.encode())
            ser.write(0)
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
                            ser.write(4)
                            time.sleep(1)
                    elif command[0] == 'RL':
                        for i in range(0, int(command[1])):
                            ser.write(1)
                            time.sleep(1)
                    elif command[0] == 'RR':
                        for i in range(0, int(command[1])):
                            ser.write(2)
                            time.sleep(1)
                    elif command[0] == 'B':
                        for i in range(0, int(command[1])):
                            ser.write(8)
                            time.sleep(1)
                ser.write(0)
            clientsocket.close()
        except:
            pass
    time.sleep(10)
