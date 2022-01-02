# Run every 15 minutes
from time import sleep

try:
    import utils.telegram_helpers as telegram_helpers
    import utils.sim800l_helpers as sim800l_helpers
    unread_sms = sim800l_helpers.read_sms(sim800l_helpers.SMS_STATUS.UNREAD)
    if len(unread_sms) > 0:
        telegram_helpers.send_message('You\'ve got mail!')
        for sms in unread_sms:
            msg_for_telegram = ''
            msg_for_telegram += f'Timestamp:\t\t{sms.timestamp}\n'
            msg_for_telegram += f'Status:\t\t{sms.status}\n'
            msg_for_telegram += f'Index:\t\t{sms.index}\n'
            msg_for_telegram += f'From:\t\t{sms.sender}\n'
            msg_for_telegram += f'SMS Content:\n{sms.text}'
            telegram_helpers.send_message(msg_for_telegram)
        sleep(1)
except:
    telegram_helpers.send_message('Error while checking for new sms messages.')