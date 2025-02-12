from ..bot import bot, tg_decorator
from ..logger import logger
from app.database.dao.telegram.user_dao import UserDAO
from app.database.models.telegram import User
from telebot.types import Message

@bot.message_handler(commands=['help'])
@tg_decorator.restricted
def invite(message: Message):
    pass