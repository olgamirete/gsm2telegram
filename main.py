import RPi.GPIO as GPIO
import utils.telegram_helpers as telegram_helpers
import utils.sim800l_helpers as sim800l_helpers

def handle_read_sms():
    sms_type = ''
    while sms_type.lower() not in ['all', 'read', 'unread']:
        sms_type = input('Read All / Read / Unread? ')
    
    sms_type = sms_type.lower()

    if sms_type == 'all':
        sms_type = sim800l_helpers.SMS_STATUS.ALL
    elif sms_type == 'read':
        sms_type = sim800l_helpers.SMS_STATUS.READ
    elif sms_type == 'unread':
        sms_type = sim800l_helpers.SMS_STATUS.UNREAD
        
    sim800l_helpers.read_sms(sms_type)
        
def handle_send_command():
    cmd = ''
    while cmd == '':
        cmd = input('Enter command to send: ')
    output = sim800l_helpers.send_command(cmd)
    print(output.text())

options = [
    ["Open serial terminal", sim800l_helpers.open_serial_terminal],
    ["Read sms", handle_read_sms],
    ["Send command", handle_send_command],
    ["Reset module", sim800l_helpers.reset_module]
]

formatted_options = [f"{str(i+1)}. {options[i][0]}" for i in range(len(options))]
formatted_options = '\n'.join(formatted_options)

interface = [
    '#-SIM800L Toolbox---------------------#',
    formatted_options,
    '\nChoose an option: '
]

while True:

    try:
        x = input('\n' + '\n'.join(interface))

        if x in [str(i+1) for i in range(len(options))]:
            i = int(x)
            selected_action = options[int(x)-1][1]
            selected_action()
        else:
            print('\nPlease select a valid option.')
    except KeyboardInterrupt:
        print('Keyboard interrput!')
    
    finally:
        GPIO.cleanup()

# telegram_helpers.send_message("test, holis3")

