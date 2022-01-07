from dotenv import load_dotenv
from os import system, getenv
from subprocess import Popen
from time import sleep

class Linphone():
    def __init__(self, default_call_address: str = None) -> None:
        self.default_call_address = default_call_address
        pass
    
    def __enter__(self):
        self.p = Popen('linphonecsh init', shell=True)
        self.p.wait()
        return self

    def __exit__(self, type, value, traceback):
        self.p.communicate('linphonecsh exit')
    
    def answer_call(self):
        self.p.communicate('linphonecsh generic "answer"')
    
    def call(self, sip_address: str = None):
        call_address = self.default_call_address | sip_address
        self.p.communicate(f'linphonecsh generic "call {call_address}"')


load_dotenv()
MY_SIP_ADDRESS = getenv('MY_SIP_ADDRESS')
print(f'sip address: {MY_SIP_ADDRESS}')

with Linphone(MY_SIP_ADDRESS) as voip:
    # sleep(5)
    voip.call()