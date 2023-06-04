import os
from dotenv import load_dotenv
import requests

# Load the environment variables from the .env file in the current directory.
load_dotenv()


class BotConfig:
    """
    This is a configuration class that sets environment variables for the bot.
    It also has a method to set the bot commands.
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

    COMMANDS_LIST = [
        {"command": "commands", "description": "Get list of commands"},
        {"command": "memes", "description": "Get meme"},
        {"command": "weather", "description": "Get current weather"},
        {"command": "add_contact", "description": "Add a contact to the phonebook"},
        {"command": "get_contact", "description": "Get a contact from the phonebook"},
        {"command": "delete_contact", "description": "Delete the contact from the phonebook"},
        # add there your other commands
    ]

    @classmethod
    def set_webhook(cls):
        """
        A class method that sets the webhook for the Telegram bot.
        It sends a POST request to the Telegram API with the webhook URL.
        If the response is successful, it prints a message indicating that the webhook has been set. 
        Otherwise, it prints a message indicating that the webhook failed to be set.
        @return None
        """
        url = BotConfig.WEBHOOK
        data = {"url": url}
        response = requests.post(f'{cls.TG_BASE_URL}{cls.BOT_TOKEN}/setWebhook', json=data)
        if response.ok:
            print('The webhook has been successfully set.')
        else:
            print('Failed to set webhook.')

    @classmethod
    def set_bot_commands(cls):
        """
        This is a class method that sets the commands for a Telegram bot. 
        It sends a POST request to the Telegram API to set the commands for the bot. 
        If the request is successful, it prints a message indicating that the commands have been set.
        Otherwise, it prints an error message.
        @return None
        """
        data = {"commands": cls.COMMANDS_LIST}
        response = requests.post(f'{cls.TG_BASE_URL}{cls.BOT_TOKEN}/setMyCommands', json=data)
        if response.ok:
            print('The commands have been successfully set.')
        else:
            print('Failed to set commands:', response.text)
