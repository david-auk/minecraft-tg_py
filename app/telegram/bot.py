import telebot
from app.telegram.config import TOKEN
from app.telegram.decorators import TelegramDecorator

bot = telebot.TeleBot(TOKEN)
tg_decorator = TelegramDecorator(bot)