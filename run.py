from tg_bot import app
from tg_bot.config import BotConfig


if __name__ == '__main__':
    """
    This code snippet is checking if the current module is being run as the main program. 
    If it is, it runs the Flask application with the specified port and debug settings from the `BotConfig` class. 
    """
    app.run(
        port=BotConfig.HOST,
        debug=BotConfig.DEBUG
    )
