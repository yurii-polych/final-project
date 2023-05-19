import json
import os
from .config import BotConfig

from tg_bot import app
import requests
from .weather_service import WeatherService, WeatherServiceException
from pprint import pprint

BOT_TOKEN = BotConfig.BOT_TOKEN
TG_BASE_URL = BotConfig.TG_BASE_URL


class User:
    def __init__(self, first_name, id, is_bot, language_code, last_name=None, username=None):
        self.first_name = first_name
        self.id = id
        self.is_bot = is_bot
        self.language_code = language_code
        self.last_name = last_name
        self.user_name = username


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
        # print(self.user)
        # print(self.user.id)

    def handle(self):
        match self.text.split():
            case 'weather', city:
                try:
                    geo_data = WeatherService.get_geo_data(city)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    # pprint(geo_data)
                    buttons = []
                    for item in geo_data:
                        test_button = {
                            'text': f'{item.get("name")} - {item.get("country_code")}',
                            'callback_data': json.dumps({
                                'lat': item.get('latitude'),
                                'lon': item.get('longitude')
                                })
                            }
                        buttons.append([test_button])

                    markup = {
                        'inline_keyboard': buttons
                        }
                    self.send_markup_message('Choose a city from a list:', markup)


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

