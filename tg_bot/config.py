import os
from dotenv import load_dotenv
import requests


load_dotenv()


class BotConfig:
    DEBUG = os.getenv('DEBUG')
    HOST = os.getenv('HOST')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    TG_BASE_URL = os.getenv('TG_BASE_URL')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    MEMES_URL = os.getenv('MEMES_URL')
    MEMES_KEY = os.getenv('MEMES_KEY')
    MEMES_HOST = os.getenv('MEMES_HOST')


commands_list = [
    {"command": "commands", "description": "Get list of commands"},
    {"command": "memes", "description": "Get 12 memes"},
    {"command": "weather", "description": "Get current weather"},
    {"command": "add_contact", "description": "Add a contact to the phonebook"},
    {"command": "get_contact", "description": "Get a contact from the phonebook"},
    {"command": "delete_contact", "description": "Delete the contact from the phonebook"},
    # add there your other commands
]


def set_bot_commands():
    data = {"commands": commands_list}
    response = requests.post(f'{BotConfig.TG_BASE_URL}{BotConfig.BOT_TOKEN}/setMyCommands', json=data)
    if response.ok:
        print('Commands set successfully!')
    else:
        print('Failed to set commands:', response.text)
