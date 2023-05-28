import json
from .config import BotConfig

from tg_bot import app, db
import requests
from .weather_service import WeatherService, WeatherServiceException
from .phonebook_service import Phonebook, PhonebookException
from pprint import pprint

from .models import UserModel

BOT_TOKEN = BotConfig.BOT_TOKEN
TG_BASE_URL = BotConfig.TG_BASE_URL


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

    def get_user_from_db(self):
        user_info = db.session.execute(db.select(UserModel).filter_by(user_id=self.id)).scalar()
        app.logger.info(f'Got user info from DB.')
        return user_info


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

    def save_last_message(self):
        user_info = self.user.get_user_from_db()
        user_info.last_message = self.text
        db.session.commit()
        app.logger.info('The last message has been saved.')

    def get_last_message(self):
        user_info = self.user.get_user_from_db()
        if user_info:
            last_message = user_info.last_message
            app.logger.info(f'Got last message: {last_message}')
            return last_message

    def undate_last_message(self):
        last_message = self.get_last_message()
        self.user.get_user_from_db().last_message = f'{last_message} {self.text}'
        db.session.commit()
        app.logger.info('Last message has been updated.')

    def delete_last_message(self):
        user_info = self.user.get_user_from_db()
        user_info.last_message = False
        db.session.commit()
        app.logger.info('Last message has been deleted.')

    def handle(self):
        match self.get_last_message():
            case '/weather':
                self.delete_last_message()
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

            case '/add_contact':  # TODO: add validation
                self.delete_last_message()
                try:
                    name, phone_number = self.text.split(' - ')
                    Phonebook.add_contact(name, phone_number, self.user.id)
                    self.send_message('Contact has been added.')
                except Exception:
                    self.send_message('Contact has not been added.')

            case '/get_contact':  # TODO: handle exception
                self.delete_last_message()
                name = self.text
                try:
                    contacts = Phonebook.get_contact(name, self.user.id)
                    if contacts:
                        for contact in contacts:
                            self.send_message(f'{contact.name} - {contact.phone_number}')
                    else:
                        self.send_message(f'No contact matching that query was found in the phone book.')
                except PhonebookException as e:
                    self.send_message(str(e))
                app.logger.info('Got the contact.')

            case '/delete_contact':
                self.delete_last_message()
                name = self.text
                Phonebook().delete_contact(name, self.user.id)
                self.send_message('Contact has been deleted successfully.')
                app.logger.info('Contact has been deleted.')

        match self.text:
            case '/start':
                try:
                    user_info = UserModel.query.filter_by(user_id=self.user.id).first()
                    if user_info is None:
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

            case '/commands':
                self.send_message('/commands \n'
                                  '/weather \n'
                                  '/add_contact \n'
                                  '/get_contact \n'
                                  '/delete_contact')

            case '/weather':
                self.save_last_message()
                self.send_message('Enter the name of the city: ')

            case '/add_contact':
                self.save_last_message()
                self.send_message(
                    'Please enter the contact details in the following format: name - phone number.'
                )

            case '/get_contact':
                self.save_last_message()
                self.send_message('Please enter the name of the contact.')

            case '/delete_contact':
                self.save_last_message()
                self.send_message('Please enter the name of the contact you want to delete.')

            case '/test':
                # self.save_last_message()
                self.get_last_message()
                # self.delete_last_message()
                # self.undate_last_message()

                self.send_message('This is message from test case.')


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
