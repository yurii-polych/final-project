import os
from dotenv import load_dotenv


load_dotenv()


class BotConfig:
    DEBUG = os.getenv('DEBUG')
    HOST = os.getenv('HOST')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    TG_BASE_URL = os.getenv('TG_BASE_URL')
