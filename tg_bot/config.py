import os
from dotenv import load_dotenv
import requests

# Load the environment variables from the .env file in the current directory.
load_dotenv()


class BotConfig:
    """
    This is a class that stores configuration variables for a bot. The variables are:
    """
    DEBUG = os.getenv('DEBUG')
    HOST = os.getenv('HOST')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    TG_BASE_URL = os.getenv('TG_BASE_URL')
    WEBHOOK = os.getenv('WEBHOOK')
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


def set_webhook():
    """
    Set the webhook for the Telegram bot to the specified URL.
    @return None.
    """
    url = BotConfig.WEBHOOK
    data = {"url": url}
    response = requests.post(f'{BotConfig.TG_BASE_URL}{BotConfig.BOT_TOKEN}/setWebhook', json=data)
    if response.ok:
        print('The webhook has been successfully set.')
    else:
        print('Failed to set webhook.')


def set_bot_commands():
    """
    This function sets the commands for a Telegram bot using the Telegram Bot API. It sends a POST request 
    to the Telegram API endpoint to set the commands for the bot. The commands are passed as a JSON object 
    in the request body. If the request is successful, it prints a success message, otherwise it prints an error message.
    @return None
    """
    data = {"commands": commands_list}
    response = requests.post(f'{BotConfig.TG_BASE_URL}{BotConfig.BOT_TOKEN}/setMyCommands', json=data)
    if response.ok:
        print('The commands have been successfully set.')
    else:
        print('Failed to set commands:', response.text)
