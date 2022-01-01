import utils.telegram_helpers as telegram_helpers
import utils.gsm_helpers as gsm_helpers

def handle_read_sms():
    sms_type = ''
    while sms_type.lower() not in ['all', 'read', 'unread']:
        
        sms_type = sms_type.lower()
        sms_type = input('Read All / Read / Unread? ')

        if sms_type == 'all':
            sms_type = gsm_helpers.SMS_STATUS.ALL
        elif sms_type == 'read':
            sms_type = gsm_helpers.SMS_STATUS.READ
        elif sms_type == 'unread':
            sms_type = gsm_helpers.SMS_STATUS.UNREAD
        
        gsm_helpers.read_sms(sms_type)
        
def handle_send_command():
    cmd = input('Enter command to send: ')
    output = gsm_helpers.send_command(cmd)
    print(output.text())

options = [
    ["Open serial terminal", gsm_helpers.open_serial_terminal],
    ["Read sms", handle_read_sms],
    ["Send command", handle_send_command]
]

formatted_options = [f"{str(i+1)}. {options[i][0]}" for i in range(len(options))]
formatted_options = '\n'.join(formatted_options)

interface = [
    '#-SIM800L Toolbox---------------------#',
    formatted_options,
    'Choose an option: '
]

while True:

    x = input('\n'.join(interface))

    options[int(x)]()

# telegram_helpers.send_message("test, holis3")

