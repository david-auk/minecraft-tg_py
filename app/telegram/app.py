import os
import telebot

# Get the bot token from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Hello, World!")

if __name__ == "__main__":
    bot.polling(none_stop=True)
