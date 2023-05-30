import requests
from tg_bot import BotConfig

MEMES_URL = BotConfig.MEMES_URL
MEMES_KEY = BotConfig.MEMES_KEY
MEMES_HOST = BotConfig.MEMES_HOST


class MemesService:
    @staticmethod
    def get_response_from_memes_service():
        url = MEMES_URL
        headers = {"X-RapidAPI-Key": MEMES_KEY, "X-RapidAPI-Host": MEMES_HOST}
        response = requests.get(url, headers=headers).json()
        return response

    def get_urls_from_response(self):
        response = self.get_response_from_memes_service()
        urls = [item.get('image') for item in response]
        return urls
