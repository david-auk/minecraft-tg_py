from ..bot import bot, tg_decorator
from ..logger import logger
from app.database.dao.telegram.user_dao import UserDAO
from app.database.models.telegram import User
from telebot.types import Message

@bot.message_handler(commands=['invite'])
@tg_decorator.restricted
def invite_command(message: Message):
    bot.reply_to(message, "📇 Send me the contact you want to invite.")
    tg_decorator.prime_listener(message.chat.id, "invite")

@tg_decorator.listener("invite")
def invite_listener(message: Message):
    if message.contact:
        contact = message.contact

        # If an invitee has no chat id (is not on TG, yet...)
        if not contact.user_id:
            bot.reply_to(message, "⚠️ Invitee does not have a telegram account, yet...")
            return

        user = User.build_from_message(message)
        invitee = User.build_from_contact(contact)

        with UserDAO() as user_dao:

            # Check if the user already exists
            if user_dao.exists(invitee.chat_id):
                bot.reply_to(message, f"✅ Contact is already authorized.")
                return

            invitee.invited_by = user  # Set the invited_by information
            user_dao.put(invitee)
            bot.reply_to(message, f"✅ Contact is now authorised!")
            logger.info(f"Invitee {invitee} Authorized by {user}")
    else:
        bot.reply_to(message, "⚠️ That was not a contact! Please send a valid contact.")


# TODO Implement remove
