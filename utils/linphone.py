from dotenv import load_dotenv
from os import system, getenv
from subprocess import Popen
from time import sleep

class Linphone():
    def __init__(self, default_call_address: str = None) -> None:
        self.default_call_address = default_call_address
        self.p = Popen('linphonec')
        self.p.wait()
    
    def answer_call(self):
        self.p.communicate('answer')
    
    def call(self, sip_address: str = None):
        call_address = self.default_call_address | sip_address
        self.p.communicate(f'call {call_address}')


load_dotenv()
MY_SIP_ADDRESS = getenv('MY_SIP_ADDRESS')

voip = Linphone(MY_SIP_ADDRESS)

sleep(5)

voip.call()