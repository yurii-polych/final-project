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


commands_list = [
    {"command": "commands", "description": "get list of commands"},
    {"command": "test", "description": "this is feature for testing"},
    {"command": "weather", "description": "get current weather"},
    {"command": "add_contact", "description": "add a contact to the phonebook"},
    {"command": "get_contact", "description": "get a contact from the phonebook"},
    {"command": "delete_contact", "description": "delete the contact from the phonebook"},
    # add there your other commands
]


def set_bot_commands():
    data = {"commands": commands_list}
    response = requests.post(f'{BotConfig.TG_BASE_URL}{BotConfig.BOT_TOKEN}/setMyCommands', json=data)
    if response.ok:
        # app.logger.info('Commands set successfully!')
        print('Commands set successfully!')
    else:
        # app.logger.error()
        print('Failed to set commands:', response.text)
