'''
Testing serial devices
'''

import serial
import time

py_serial = serial.Serial(port='/dev/ttyACM0',baudrate=9600)
time.sleep(1)

while True:
      
    command = input('command:')
    #print(command.encode())
    #py_serial.write(b'0')
    py_serial.write(command.encode())

    time.sleep(3)
    
    if py_serial.readable():

        response = py_serial.readline()
        
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        print(response.decode())
