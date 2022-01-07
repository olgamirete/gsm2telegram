from dotenv import load_dotenv
from os import system, getenv
from subprocess import Popen, PIPE
from time import sleep

class Linphone():
    def __init__(self, default_call_address: str = None, timeout: int = 10) -> None:
        self.default_call_address = default_call_address
        self.TIMEOUT = timeout
    
    def __enter__(self):
        self.p = Popen('linphonecsh init', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
        print('Initiated successfully!')
        return self

    def __exit__(self, type, value, traceback):
        outs, errs = self.p.communicate('linphonecsh exit', timeout=self.TIMEOUT)
        self.p.kill()
        print('Exited correctly!')
    
    def answer_call(self):
        outs, errs = self.p.communicate('linphonecsh generic "answer"', timeout=self.TIMEOUT)
    
    def call(self, sip_address: str = None):
        call_address = self.default_call_address if sip_address == None else sip_address
        print(f'Will make a call to {call_address}!')
        outs, errs = self.p.communicate(f'linphonecsh generic "call {call_address}"', timeout=self.TIMEOUT)
        print(outs)
        print(errs)
        sleep(30)


load_dotenv()
MY_SIP_ADDRESS = getenv('MY_SIP_ADDRESS')
print(f'sip address: {MY_SIP_ADDRESS}')

with Linphone(MY_SIP_ADDRESS) as voip:
    # sleep(5)
    voip.call()

    # a = input('Press enter to end.')