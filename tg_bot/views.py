from tg_bot import app
from flask import request

from .handlers import MessageHandler, CallbackHandler


@app.route('/', methods=["POST"])
def hello():
    """
    This is a Flask route that listens for incoming POST requests.
    f the request contains a JSON object with a "message" key,
    it creates a MessageHandler object and calls its handle() method.

    If the request contains a JSON object with a "callback_query" key,
    it creates a CallbackHandler object and calls its handle() method.
    In either case, it returns the string "Ok".
    """
    if message := request.json.get('message'):
        handler = MessageHandler(message)
        handler.handle()
    elif callback := request.json.get('callback_query'):
        handler = CallbackHandler(callback)
        handler.handle()

    return 'Ok'
