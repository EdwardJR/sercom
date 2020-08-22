import serial
from time import sleep
import struct

values = (1,2,3,4,5)

string = b''

for i in values:
    string += struct.pack('!B',i)

print(string)
ser = serial.Serial(port='COM3', baudrate=9600)
ser.close()
ser.open()
sleep(5)
for i in range(3):
	ser.write(b'\x01')

ser.close()
