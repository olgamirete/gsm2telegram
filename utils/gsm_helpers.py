import serial
import RPi.GPIO as GPIO
from time import sleep

SERIAL_PORT = "/dev/ttyAMA0"

GPIO.setmode(GPIO.BOARD)

class GSMInitializationError(Exception):
    pass

# class GSMError(Exception):
#     pass

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
                serial_str = piSerial.readline().decode('utf-8')
                if serial_str.endswith('\n\r'):
                    line_constructor += serial_str[:-2]
                    line = line_constructor
                    line_constructor = ''
                    print(line)
                    if serial_str.endswith('OK\n\r'):
                        break
                    if serial_str.endswith('ERROR\n\r'):
                        break
                else:
                    line_constructor += serial_str
                    print('Still constructing output, waiting for \\n\\r chars...')
                    print('Here is what has been received now:')
                    print(serial_str)
                sleep(1)

            cmd = input('Insert command (or press enter to quit): ')

def reset_module():
    confirm = input('Do you really want to reset the GSM Module? (y/n): ')
    if confirm.lower() == 'y':
        raise NotImplemented