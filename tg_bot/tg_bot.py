import config
import telebot
from .bot.bot import on_message

bot = telebot.TeleBot(config.TOKEN, threaded=True)


@bot.message_handler(content_types=["text"])
def message_came(message):
    on_message(bot, message.text, message.chat.username, message.chat.id)
