import os
import telebot
from . import decorators

# Get the bot token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
tg_decorator = decorators.TelegramDecorator(bot)

@bot.message_handler(func = lambda message: True)
@tg_decorator.authorised_arg
def echo_all(message):
    bot.reply_to(message, "Hello, World!")


if __name__ == "__main__":
    bot.polling(none_stop = True)
