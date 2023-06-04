from flask import Flask
from logging.config import dictConfig
from .config import BotConfig
from flask_sqlalchemy import SQLAlchemy

# This code initializes a SQLAlchemy object, which is a toolkit and ORM (Object-Relational Mapping) for Python. 
# It provides a set of high-level API to interact with relational databases.
db = SQLAlchemy()
    

app = Flask(__name__)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Load the configuration settings for the Flask app from the BotConfig object.
app.config.from_object(BotConfig)

BotConfig.set_webhook()

BotConfig.set_bot_commands()

db.init_app(app)


from .views import *
from .models import *


with app.app_context():
    db.create_all()
