# Run every 15 minutes
from time import sleep
from os import path
import utils.telegram_helpers as telegram_helpers
import utils.sim800l_helpers as sim800l_helpers
from utils.logger import Logger

logs_folder = path.join(path.dirname(__file__), 'logs')
logger = Logger('sms_watchdog', logs_folder)

try:
    unread_sms = sim800l_helpers.read_sms(sim800l_helpers.SMS_STATUS.UNREAD)
    if len(unread_sms) > 0:
        telegram_helpers.send_message(f'**You\'ve got SMS!**\nFound {len(unread_sms)} message/s.')
        logger.log(f'Found {len(unread_sms)} message/s.')
        for sms in unread_sms:
            msg_for_telegram = ''
            msg_for_telegram += f'```Timestamp:   ```{sms.timestamp}\n'
            msg_for_telegram += f'```Status:      ```{sms.status}\n'
            msg_for_telegram += f'```Index:       ```{sms.index}\n'
            msg_for_telegram += f'```From:        ```{sms.sender}\n'
            msg_for_telegram += f'```SMS Content:```\n{sms.text}'
            telegram_helpers.send_message(msg_for_telegram)
        sleep(1)
    else:
        logger.log('No messages found.')
except Exception as e:
    msg_constructor = [
        '**Error** while checking for new sms messages.',
        '__Error message:__',
        e
    ]
    error_msg = '\n\n'.join(msg_constructor)
    logger.log(f'Error while checking for new SMS. See {logger.ERROR_LOG_FILE} file for detail.')
    logger.log_error(e)
    telegram_helpers.send_message(error_msg)
    