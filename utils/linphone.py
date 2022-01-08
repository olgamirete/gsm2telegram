from dotenv import load_dotenv
from os import system, getenv
# from subprocess import Popen, PIPE
from time import sleep

class Linphone():
    def __init__(self, default_call_address: str = None, timeout: int = 10) -> None:
        self.default_call_address = default_call_address
        self.TIMEOUT = timeout
    
    def __enter__(self):
        system('linphonecsh init -c ~/.linphonerc')
        # cmds = [
        #     'proxy add',
        #     '<sip:sip.linphone.org;transport=tls>' # Proxy sip address
        #     'sip:fgiancarelli_caller@sip.linphone.org', # Username / Identity for proxy
        #     'yes' # "Do you want to register on this proxy?"
        #     '0', # "Specify register expiration time in seconds (default is 600)"
        #     '', # "Specify route if needed",
        #     "yes" # Accept proxy configuration
        # ]
        print('Initiated successfully!')
        return self

    def __exit__(self, type, value, traceback):
        system('linphonecsh exit')
        print('Exited correctly!')
    
    def answer_call(self):
        system('linphonecsh generic "answer"')
    
    def call(self, sip_address: str = None):
        call_address = self.default_call_address if sip_address == None else sip_address
        print(f'Will make a call to {call_address}!')
        system(f'linphonecsh generic "call {call_address}"')
        sleep(10)
        # print(outs)
        # print(errs)


load_dotenv()
MY_SIP_ADDRESS = getenv('MY_SIP_ADDRESS')
print(f'sip address: {MY_SIP_ADDRESS}')

with Linphone(MY_SIP_ADDRESS) as voip:
    # sleep(5)
    voip.call()

    # a = input('Press enter to end.')
    print("finished call")