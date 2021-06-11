import telebot
from bot.logic import on_message


TOKEN = "1735621189:AAFhwupBv2WNM4n0QdmbKgM8xQXCIySsaTw"

bot = telebot.TeleBot(TOKEN, threaded=False)


@bot.message_handler(content_types=["text"])
def message_came(message):
    if message.chat.username:
        on_message(bot, message.text, message.chat.username, message.chat.id)
    else:
        on_message(bot, message.text, f"id{str(message.chat.id)}", message.chat.id)


if __name__ == '__main__':
    print("Bot started!")
    while True:
        # try:
        bot.polling(none_stop=True, timeout=3)
        # except Exception as e:
        #     print(type(e))
        #     time.sleep(3)
