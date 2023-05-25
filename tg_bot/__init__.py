from flask import Flask
from .config import BotConfig
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

app.config.from_object(BotConfig)

db.init_app(app)

from .views import *
from .models import *


with app.app_context():
    db.create_all()
