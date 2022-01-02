import serial
import RPi.GPIO as GPIO
from time import sleep, time
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SERIAL_PORT = getenv("SERIAL_PORT")
SERIAL_BAUD = 9600
SERIAL_TIMEOUT = 5
PAUSE_AFTER_SERIAL_OPEN = 2
PAUSE_BEFORE_SERIAL_READ = .5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.OUT) # RST pin
GPIO.output(17, 1)       # Normally high.

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

class Received_SMS():
    def __init__(self, text: str = None, sender: str = None, timestamp: str = None, index: int = None, status: SMS_STATUS = None) -> None:
        self.text = text
        self.sender = sender
        self.timestamp = timestamp
        self.index = index
        self.status = status

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
        GPIO.output(17, 0)
        sleep(.003)
        GPIO.output(17, 1)

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
    print(f'Setting AT+CMGF={1 if flag_text_mode == True else 0}...')
    output = send_command(f'AT+CMGF={1 if flag_text_mode == True else 0}')
    print('Finished configuring AT+CMGF!')
    if output.status == 'OK':
        print('Retrieving messages...')
        output = send_command(f'AT+CMGL="{filter_by_status}"')
        print('Finished retrieving messages! Now parsing...')
        messages = __parse_sms(output._lines)
        print('Finished parsing messages! See results:')
        print(f'Found {len(messages)} message/s.')
        if len(messages) > 0:
            for i in range(len(messages)):
                msg = messages[i]
                print('----------------------------------------------------')
                print(f'Timestamp:\t{msg.timestamp}')
                print(f'Status:\t{msg.status}')
                print(f'Index:\t{msg.index}')
                print(f'From:\t{msg.sender}')
                print(f'SMS Content:\n{msg.text}')
        
        print(output.text())
    else:
        print('Error while setting the SMS mode. See answer from GSM module:')
        print(output.text())

def __parse_sms(serial_lines: list[str]) -> list[Received_SMS]:
    list_of_sms = []
    sms = None
    for i in range(len(serial_lines)):
        line = serial_lines[i]
        if line.startswith('+CMGL: '):
            
            if sms != None:
                list_of_sms.append(sms)
                sms = None

            line_split_by_comma = line.split(',')
            
            index = line[8:line.find(',')]
            status = line_split_by_comma[1].replace('"', '')
            sender = line_split_by_comma[2].replace('"', '')
            timestamp = f'{line_split_by_comma[-2]}T{line_split_by_comma[-1]}'
            timestamp = timestamp.replace('/', '-')
            
            sms = Received_SMS(
                text='',
                sender=sender,
                timestamp=timestamp,
                index=index,
                status=status
            )
        else:
            if sms == None:
                print('Unhandled line found. See line below:')
                print(line)
            else:
                sms.text += line
    list_of_sms.append(sms)
    return list_of_sms
            

