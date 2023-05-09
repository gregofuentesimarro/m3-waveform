import serial
from time import sleep

device = serial.Serial('COM5')
sleep(1) 

device.write(b'IDN\n')
answer = device.readline()
print(f'The answer is: {answer}')
device.close()
print('Device closed')
