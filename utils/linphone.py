from dotenv import load_dotenv
from os import system, getenv

class Linphone():
    def __init__(self, default_call_address: str = None) -> None:
        self.default_call_address = default_call_address
        system('linphonec')
    
    def answer_call(self):
        system('answer')
    
    def call(self, sip_address: str = None):
        call_address = self.default_call_address | sip_address
        system(f'call {call_address}')


load_dotenv()
MY_SIP_ADDRESS = getenv('MY_SIP_ADDRESS')

voip = Linphone(MY_SIP_ADDRESS)

voip.call()