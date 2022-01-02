import serial
import RPi.GPIO as GPIO
from time import sleep
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SERIAL_PORT = getenv("SERIAL_PORT")
SERIAL_BAUD = 9600
SERIAL_TIMEOUT = 5
PAUSE_AFTER_SERIAL_OPEN = 2
PAUSE_BEFORE_SERIAL_READ = .5

class SMS_STATUS:
    ALL = "ALL"
    READ = "REC READ"
    UNREAD = "REC UNREAD"

class AT_COMMAND_OUTPUT:
    def __init__(self) -> None:
        self.status = None
        self._lines = []
    
    def setStatus(self, newStatus: str):
        self.status = newStatus
    
    def addLine(self, newLine: str):
        self._lines.append(newLine)

    def text(self):
        return '\n'.join(self._lines)

GPIO.setmode(GPIO.BOARD)

class GSMInitializationError(Exception):
    pass

def _write_to_serial(ser: serial.Serial, command: str):
    ser.write(command.encode('utf-8'))

def open_serial_terminal():
    with serial.Serial(SERIAL_PORT, baudrate=SERIAL_BAUD, timeout=SERIAL_TIMEOUT) as piSerial:
        sleep(PAUSE_AFTER_SERIAL_OPEN)
        _write_to_serial(piSerial, 'AT\r\n')
        sleep(PAUSE_BEFORE_SERIAL_READ)
        while True:
            line = piSerial.readline().decode('utf-8')
            if line == 'OK\r\n':
                print('Correctly initialized communication with GSM module!')
                break
            if line == 'ERROR\r\n':
                raise GSMInitializationError
            sleep(PAUSE_BEFORE_SERIAL_READ)

        cmd = input('Insert command (or press enter to quit): ')
        while cmd != '':
            _write_to_serial(piSerial, f'{cmd}\r\n')
            sleep(PAUSE_BEFORE_SERIAL_READ)
            line_constructor = ''
            while True:
                serial_str = piSerial.readline().decode('utf-8')
                if serial_str.endswith('\r\n'):
                    line_constructor += serial_str[:-2]
                    line = line_constructor
                    line_constructor = ''
                    print(line)
                    if serial_str == 'OK\r\n':
                        break
                    if serial_str == 'ERROR\r\n':
                        break
                else:
                    line_constructor += serial_str
                    print('Still constructing output, waiting for \\r\\n chars...')
                sleep(PAUSE_BEFORE_SERIAL_READ)

            cmd = input('Insert command (or press enter to quit): ')

def reset_module():
    confirm = input('Do you really want to reset the GSM Module? (y/n): ')
    if confirm.lower() == 'y':
        raise NotImplemented

def send_command(cmd: str, encoding_for_decoding: str = 'utf-8'):

    if not cmd.endswith('\r\n'):
        cmd += '\r\n'
    
    with serial.Serial(SERIAL_PORT, baudrate=SERIAL_BAUD, timeout=SERIAL_TIMEOUT) as piSerial:
        sleep(PAUSE_AFTER_SERIAL_OPEN)
        _write_to_serial(piSerial, 'AT\r\n')
        sleep(PAUSE_BEFORE_SERIAL_READ)
        while True:
            line = piSerial.readline().decode('utf-8')
            if line == 'OK\r\n':
                # Correctly initialized communication with GSM module!
                break
            if line == 'ERROR\r\n':
                raise GSMInitializationError
            sleep(PAUSE_BEFORE_SERIAL_READ)
        
        _write_to_serial(piSerial, cmd)
        sleep(PAUSE_BEFORE_SERIAL_READ)

        output = AT_COMMAND_OUTPUT()
        line_constructor = ''
        while True:
            serial_str = piSerial.readline().decode(encoding_for_decoding)
            if serial_str.endswith('\r\n'):
                line_constructor += serial_str[:-2]
                line = line_constructor
                line_constructor = ''
                output.addLine(line)
                if serial_str == 'OK\r\n':
                    output.setStatus('OK')
                    break
                if serial_str == 'ERROR\r\n':
                    output.setStatus('ERROR')
                    break
            else:
                line_constructor += serial_str
                # Still constructing output, waiting for \\r\\n chars...
            sleep(PAUSE_BEFORE_SERIAL_READ)
        return output

def read_sms(filter_by_status: SMS_STATUS = SMS_STATUS.UNREAD, flag_text_mode: bool = True):
    if flag_text_mode == True:
        output = send_command('AT+CMGF=1')
    else:
        output = send_command('AT+CMGF=0')
    if output.status == 'OK':
        output = send_command(f'AT+CMGL="{filter_by_status}"')
        print(output.text())
    else:
        print('Error while setting the SMS mode. See answer from GSM module:')
        print(output.text())