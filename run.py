from tg_bot import app
from tg_bot.config import BotConfig


if __name__ == '__main__':
    app.run(
        port=BotConfig.HOST,
        debug=BotConfig.DEBUG
    )
