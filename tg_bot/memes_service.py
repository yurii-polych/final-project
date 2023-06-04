import requests
from tg_bot import BotConfig

MEMES_URL = BotConfig.MEMES_URL
MEMES_KEY = BotConfig.MEMES_KEY
MEMES_HOST = BotConfig.MEMES_HOST


class MemesServiceException(Exception):
    pass


class MemesService:
    """
    This class provides a service to retrieve memes from a remote API. It has two methods:
    1. `get_response_from_memes_service()`: This method sends a GET request to the remote API
        and returns the response in JSON format.
    2. `get_urls_from_response()`: This method calls `get_response_from_memes_service()` to get the response
        from the remote API, extracts the URLs of the memes from the response, and returns them as a list.
    """
    URLS = []

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

    def get_one_url(self):
        if not self.URLS:
            urls = self.get_urls_from_response()
            self.URLS += urls
        one_url = self.URLS.pop()
        return one_url
