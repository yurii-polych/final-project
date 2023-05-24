import json
import os
from .config import BotConfig

from tg_bot import app
from tg_bot import db
import requests
from .weather_service import WeatherService, WeatherServiceException
from pprint import pprint

from .models import UserModel

BOT_TOKEN = BotConfig.BOT_TOKEN
TG_BASE_URL = BotConfig.TG_BASE_URL
IS_SEARCHING = False


class User:
    def __init__(self, first_name, id, is_bot, language_code, last_name=None, username=None):
        self.first_name = first_name
        self.id = id
        self.is_bot = is_bot
        self.language_code = language_code
        self.last_name = last_name
        self.username = username

    def register_new_user_in_db(self):
        new_user = UserModel(
            user_id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username
        )
        db.session.add(new_user)
        db.session.commit()


class TelegramHandler:
    user = None

    def send_markup_message(self, text, markup):
        data = {
            'chat_id': self.user.id,
            'text': text,
            'reply_markup': markup
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)

    def send_message(self, text):
        data = {
            'chat_id': self.user.id,
            'text': text
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)


class MessageHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def handle(self):
        global IS_SEARCHING

        match IS_SEARCHING:
            case True:
                IS_SEARCHING = False
                try:
                    geo_data = WeatherService.get_geo_data(self.text)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    # pprint(geo_data)
                    buttons = []
                    for item in geo_data:
                        button = {
                            'text': f'{item.get("name")} - {item.get("country_code")}',
                            'callback_data': json.dumps({
                                'lat': item.get('latitude'),
                                'lon': item.get('longitude')
                            })
                        }
                        buttons.append([button])

                    markup = {
                        'inline_keyboard': buttons
                    }
                    self.send_markup_message('Choose a city from a list:', markup)

        match self.text:
            case '/weather':
                self.send_message('Enter the name of the city: ')
                IS_SEARCHING = True

            case '/start':
                try:
                    user_id = UserModel.query.filter_by(user_id=self.user.id).first()
                    if user_id is None:
                        self.user.register_new_user_in_db()
                        start_speach = "Hello, I am NailsMaster Bot. \n" \
                                       "Please select a command from the 'Menu' button."
                        self.send_message(start_speach)
                    else:
                        message_to_existed_user = "I'm glad you're back. \n" \
                                                  "Please select a command from the 'Menu' button."
                        self.send_message(message_to_existed_user)
                except Exception as e:
                    self.send_message(str(e))


class CallbackHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.callback_data = json.loads(data.get('data'))

    def handle(self):
        try:
            weather = WeatherService.get_current_weather_by_geo_data(**self.callback_data)
        except WeatherServiceException as wse:
            self.send_message(str(wse))
        else:
            # self.send_message(json.dumps(weather))
            self.send_message(weather)
