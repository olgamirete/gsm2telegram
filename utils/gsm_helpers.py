import serial
import RPi.GPIO as GPIO
from time import sleep

SERIAL_PORT = "/dev/ttyAMA0"

GPIO.setmode(GPIO.BOARD)

class GSMInitializationError(Exception):
    pass

def _write_to_serial(ser: serial.Serial, command: str):
    ser.write(command.encode('utf-8'))

def open_serial_terminal():
    #Open port with baud rate
    with serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5) as piSerial:
        sleep(3)
        _write_to_serial(piSerial, 'AT\r\n')
        sleep(1)
        while True:
            line = piSerial.readline().decode('utf-8')
            if line == 'OK\r\n':
                print('Correctly initialized communication with GSM module!')
                break
            if line == 'ERROR\r\n':
                raise GSMInitializationError
            sleep(1)

        cmd = input('Insert command (or press enter to quit): ')
        while cmd != '':
            _write_to_serial(piSerial, f'{cmd}\r\n')
            sleep(1)
            line_constructor = ''
            while True:
                line_constructor += piSerial.readline().decode('utf-8')
                if line_constructor.endswith('\n\r'):
                    line = line_constructor[:-2]
                    line_constructor = ''
                    print(line)
                    if line == 'OK':
                        break
                    if line == 'ERROR':
                        break
                else:
                    print('Still constructing output, waiting for \\n\\r chars...')
                sleep(1)

            cmd = input('Insert command (or press enter to quit): ')
