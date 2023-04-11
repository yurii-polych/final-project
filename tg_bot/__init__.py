from flask import Flask
from .config import BotConfig


app = Flask(__name__)

app.config.from_object(BotConfig)


from .views import *
