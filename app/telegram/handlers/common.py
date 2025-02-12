from ..bot import bot
from ..logger import logger
from app.database.dao.telegram.user_dao import UserDAO
from app.database.models.telegram import User
from telebot.types import Message

def not_registered_response(message: Message):
    bot.reply_to(
        message,
        "⚠️ You are **not registered** to use this bot.\n"
        "❓ Please ask the admin to invite you using `/invite`."
    )

@bot.message_handler(commands=['start'])
def start_command(message: Message):
    """Handler for start command."""

    user = User.build_from_message(message)

    logger.info(f"User {user} started the bot.")

    with UserDAO() as user_dao:
        first_to_start = len(user_dao.get_all()) == 0
        if first_to_start:
            logger.info(f"User {user} added to database, due to them being the first user.")
            user_dao.put(user)
            bot.reply_to(message,
                "🎉 You are the **first user**! You have been **promoted to admin**.\n\n"
                "✅ Use `/invite` to invite others by sharing their contact.\n"
                "ℹ️ Use `/help` to see available commands."
            )
        else:
            if user_dao.exists(user.chat_id):
                bot.reply_to(message,
                    "👋 Hello! Welcome to the bot.\n\n"
                    "🔹 Use /help to see what I can do!\n"
                    "🔹 Send me any message, and I'll reply!"
                )
            else:
                logger.info(f"User {user} not registered yet.")
                not_registered_response(message)


@bot.message_handler(commands=['help'])
def help_command(message: Message):
    """Handler for printing a useful help command."""

    user = User.build_from_message(message)

    logger.info(f"User {user} requested help.")
    bot.send_chat_action(message.chat.id, 'typing')
    with UserDAO() as user_dao:
        if user_dao.exists(message.chat.id):
            bot.reply_to(
                message,
                "🛠 **Available Commands:**\n"
                "/start - Start interacting with me 🤖\n"
                "/help - Show this help message 📖\n"
                "/echo [message] - Repeat your message 🔁"
            )
        else:
            not_registered_response(message)

@bot.message_handler(func=lambda message: message.text.startswith("/"))
def unknown_command(message: Message):
    logger.warning(f"Unknown command from {message.chat.id}: {message.text}")
    bot.reply_to(message, "⚠️ Unknown command. Type /help to see available commands.")