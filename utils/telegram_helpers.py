from os import getenv
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

class UserNotFoundException(Exception):
    pass

def send_message(msg: str, to_user_id: int = None):

    user_id = getenv("MY_USER_ID") if to_user_id == None else to_user_id
    # Create a new Client instance
    app = Client(
        "my_account",
        api_id=getenv("API_ID"),
        api_hash=getenv("API_HASH")
    )

    with app:
        # Send a message, Markdown is enabled by default
        app.send_message(user_id, msg)
        # Send a location
        # app.send_location(user_id, 51.500729, -0.124583)
        # contacts = app.get_contacts()
        # print(contacts)

def send_document(filepath: str, to_user_id: int = None):

    user_id = getenv("MY_USER_ID") if to_user_id == None else to_user_id
    # Create a new Client instance
    app = Client(
        "my_account",
        api_id=getenv("API_ID"),
        api_hash=getenv("API_HASH")
    )

    with app:
        # Send a message, Markdown is enabled by default
        app.send_document(user_id, document=filepath)
        # Send a location
        # app.send_location(user_id, 51.500729, -0.124583)
        # contacts = app.get_contacts()
        # print(contacts)
    
def find_user_id_by_msg(msg: str):
    # Create a new Client instance
    app = Client(
        "my_account",
        api_id=getenv("API_ID"),
        api_hash=getenv("API_HASH")
    )

    with app:
        messages = app.search_global(query=msg)
    
    if len(messages) > 0:
        return messages[0]["from_user"]["id"]
    else:
        raise UserNotFoundException
