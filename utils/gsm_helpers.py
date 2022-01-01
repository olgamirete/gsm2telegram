import serial
import RPi.GPIO as GPIO
from time import sleep

SERIAL_PORT = "/dev/ttyAMA0"

GPIO.setmode(GPIO.BOARD)

def _write_to_serial(ser: serial.Serial, command: str):
    ser.write(command.encode())

def get_unread_sms():
    #Open port with baud rate
    with serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5) as piSerial:
        sleep(1)
        _write_to_serial(piSerial, 'AT+CMGL="REC UNREAD"')
        # The response should be something like this:

        # +CMGL: 1,"REC UNREAD","+85291234567",,"07/02/18,00:05:10+32"
        # Reading text messages is easy.
        # +CMGL: 2,"REC UNREAD","+85291234567",,"07/02/18,00:07:22+32"
                
        response_lines = piSerial.readlines()

        for x in response_lines:
            print(x.decode())
        
        # for i in range(len(response_lines)/2):

        
        # while True:

