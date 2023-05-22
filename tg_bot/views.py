import requests
import datetime
from pprint import pprint

from tg_bot import app
from flask import request

from .handlers import MessageHandler, CallbackHandler


@app.route('/', methods=["POST"])
def hello():
    # pprint(f'First print in route: {datetime.datetime.now()}')
    if message := request.json.get('message'):
        # pprint(request.json)
        # pprint(f'2 print in route: {datetime.datetime.now()}')
        handler = MessageHandler(message)
        handler.handle()
    elif callback := request.json.get('callback_query'):
        # pprint(f'3 print in route: {datetime.datetime.now()}')
        handler = CallbackHandler(callback)
        handler.handle()

    return 'Ok'
