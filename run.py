from tg_bot import app
from tg_bot.config import BotConfig


app.run(
    port=BotConfig.HOST,
    debug=BotConfig.DEBUG
)
