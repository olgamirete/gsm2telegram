from dotenv import load_dotenv
from os import getenv, system

load_dotenv()

MY_SIP_ADDRESS = getenv('MY_SIP_ADDRESS')

def call_me():
    system(f'linphonec -s {MY_SIP_ADDRESS}')
