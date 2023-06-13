import json
import requests

from tg_bot import app, db, BotConfig
from .weather_service import WeatherService, WeatherServiceException
from .phonebook_service import Phonebook, PhonebookException
from .memes_service import MemesService, MemesServiceException
from .models import UserModel


BOT_TOKEN = BotConfig.BOT_TOKEN
TG_BASE_URL = BotConfig.TG_BASE_URL


class User:
    """
    This code defines a User class with an __init__ method that initializes the user's attributes such as
    first name, id, is_bot, language_code, last_name, and username.
    """
    
    def __init__(self, first_name, id, is_bot, language_code, last_name=None, username=None):
        self.first_name = first_name
        self.id = id
        self.is_bot = is_bot
        self.language_code = language_code
        self.last_name = last_name
        self.username = username

    def register_new_user_in_db(self):
        """
        This method registers a new user in the database by creating a new UserModel object with the user's information, 
        adding it to the database session, and committing the changes to the database.
        :return None
        """
        new_user = UserModel(
            user_id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username
        )
        db.session.add(new_user)
        db.session.commit()

    def get_user_from_db(self):
        """
        This method retrieves user information from the database based on the user ID.
        :param self - the instance of the class calling the method
        :return user_info - the user information retrieved from the database
        """
        user_info = db.session.execute(db.select(UserModel).filter_by(user_id=self.id)).scalar()
        app.logger.info(f'Got user info from DB.')
        return user_info


class TelegramHandler:
    """
    This is a class that handles sending messages and images to a user via Telegram API. 
    """
    user = None

    def send_markup_message(self, text, markup):
        """
        This method sends a message with markup to a user via Telegram API.
        :param self - the instance of the class
        :param text - the text message to be sent
        :param markup - the markup to be sent with the message
        :return None
        """
        data = {
            'chat_id': self.user.id,
            'text': text,
            'reply_markup': markup
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)

    def send_message(self, text):
        """
        This method sends a message to a user via Telegram Bot API.
        :param self - the instance of the class
        :param text - the message to be sent
        :return None
        """
        data = {
            'chat_id': self.user.id,
            'text': text
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)

    def send_image(self, url):
        """
        Given a URL, send an image to a user via Telegram.
        :param self - the instance of the class
        :param url - the URL of the image to be sent
        :return None
        """
        data = {
            "chat_id": f"{self.user.id}",
            "photo": url
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendPhoto', json=data)


class MessageHandler(TelegramHandler):
    """
    This is a class that handles incoming messages from Telegram. 
    It has an `__init__` method that takes in data and initializes the user and text attributes. 
    It also has a `save_last_message` method that saves the last message sent by the user to the database. 
    """
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def save_last_message(self):
        """
        This method saves the last message sent by the user to the database.
        It retrieves the user information from the database, updates the last message
        field with the current message, and commits the changes to the database.
        :param self - the instance of the class
        :return None
        """
        user_info = self.user.get_user_from_db()
        if user_info:
            user_info.last_message = self.text
            db.session.commit()
            app.logger.info('The last message has been saved.')

    def get_last_message(self):
        """
        This method retrieves the last message sent by the user from the database.
        It first retrieves the user information from the database and then returns the last message sent by the user.
        If the user information is not found in the database, it returns None.
        :return The last message sent by the user.
        """
        user_info = self.user.get_user_from_db()
        if user_info:
            last_message = user_info.last_message
            app.logger.info(f'Got last message: {last_message}')
            return last_message

    def update_last_message(self):
        """
        This method updates the last message of a user in the database with the current message. 
        It first retrieves the last message from the database using the `get_last_message()` method. 
        It then appends the current message to the last message and updates the user's `last_message` field
        in the database.
        Finally, it commits the changes to the database and logs that the last message has been updated.
        :return None
        """
        last_message = self.get_last_message()
        self.user.get_user_from_db().last_message = f'{last_message} {self.text}'
        db.session.commit()
        app.logger.info('Last message has been updated.')

    def delete_last_message(self):
        """
        This method deletes the last message sent by the user. 
        It does this by retrieving the user's information from the database, setting the `last_message` attribute
        to `False`, and then committing the changes to the database.
        Finally, it logs a message indicating that the last message has been deleted.
        :param self - the instance of the class
        :return None
        """
        user_info = self.user.get_user_from_db()
        user_info.last_message = False
        db.session.commit()
        app.logger.info('Last message has been deleted.')

    def handle(self):
        """
        This is a method that handles incoming messages.
        It checks the last message received and performs different actions based on the message type.
        :return None
        """
        match self.get_last_message():
            case '/weather':
                """
                This code is part of a chatbot that responds to user messages. 
                If the last message matches '/weather', it will delete the last message and attempt to retrieve 
                geo data from a weather service. 
                If the service returns an exception, the bot will send the exception message to the user. 
                Otherwise, it will create a list of buttons for each city in the geo data and send a message 
                to the user with the list of buttons to choose from.
                :return None
                """
                self.delete_last_message()
                try:
                    geo_data = WeatherService.get_geo_data(self.text)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
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

            case '/add_contact':
                self.delete_last_message()
                try:
                    if not ' - ' in self.text:
                        raise self.send_message('Please use " - " separator.')
                    name, phone_number = self.text.split(' - ')
                    if not Phonebook.validate_phone_number(phone_number):
                        raise self.send_message('Invalid phone number. \n'
                                                'The phone number should be in the format +XXXXXXXXXXXX or XXXXXXXXXXX.')
                    Phonebook.add_contact(name, phone_number, self.user.id)
                except Exception:
                    self.send_message('Contact has not been added. Please enter correct data.')
                else:
                    self.send_message('Contact has been added.')

            case '/get_contact':
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
                else:
                    app.logger.info('Got the contact.')

            case '/delete_contact':
                self.delete_last_message()
                name = self.text
                try:
                    Phonebook().delete_contact(name, self.user.id)
                except Exception as e:
                    app.logger.error('Contact has not been deleted.')
                    self.send_message(str(e))
                else:
                    self.send_message('Contact has been deleted successfully.')
                    app.logger.info('Contact has been deleted.')

        match self.text:
            case '/start':
                """
                This code appears to be a part of a chatbot's response to user input. 
                """
                try:
                    user_info = UserModel.query.filter_by(user_id=self.user.id).first()
                    if user_info is None:
                        self.user.register_new_user_in_db()
                        start_speach = "Hello, I am Meme Bot. \n" \
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
                                  '/memes \n'
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

            case '/memes':
                self.send_message('IT meme is coming.')
                try:
                    meme = MemesService().get_one_url()
                except MemesServiceException as e:
                    self.send_message(str(e))
                else:
                    self.send_image(meme)
                    app.logger.info('Got meme.')

            case _:
                self.send_message('Unrecognized command. \nPlease select a command from the list: \n'
                                  '/commands \n'
                                  '/weather \n'
                                  '/memes \n'
                                  '/add_contact \n'
                                  '/get_contact \n'
                                  '/delete_contact')


class CallbackHandler(TelegramHandler):
    """
    This is a class that handles callbacks from a Telegram bot. 
    It takes in data from the callback and initializes a `User` object and a `callback_data` dictionary. 
    It then attempts to get the current weather using the `WeatherService` class and the `callback_data` dictionary. 
    If there is an exception, it sends a message with the error.
    If there is no exception, it sends a message with the current weather.
    """
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.callback_data = json.loads(data.get('data'))

    def handle(self):
        try:
            weather = WeatherService.get_current_weather_by_geo_data(**self.callback_data)
        except WeatherServiceException as wse:
            self.send_message(str(wse))
        else:
            self.send_message(weather)
