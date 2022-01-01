import serial
import RPi.GPIO as GPIO
from time import sleep

SERIAL_PORT = "/dev/ttyAMA0"

GPIO.setmode(GPIO.BOARD)

def _write_to_serial(ser: serial.Serial, command: str):
    ser.write(command.encode('utf-8'))
    sleep(3)

def get_unread_sms():
    #Open port with baud rate
    with serial.Serial(SERIAL_PORT, baudrate=9600, timeout=5) as piSerial:
        sleep(3)
        _write_to_serial(piSerial, 'AT\r\n')
        sleep(1)
        while True:
            line = piSerial.readline().decode('utf-8')
            print(line)
            if line == 'OK\r\n':
                break
            if line == 'ERROR\r\n':
                break
            sleep(1)
        print('Correctly initialized communication!')

        cmd = input('Insert command (or press enter to quit): ')
        while cmd != '':
            # 'AT+CMGL="REC UNREAD"\r\n'
            
            _write_to_serial(piSerial, f'{cmd}\r\n')
            # print("Written to serial!")

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
            
        