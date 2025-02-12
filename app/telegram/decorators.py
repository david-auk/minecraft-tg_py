from functools import wraps

from telebot import TeleBot
from app.database.dao.telegram.user_dao import UserDAO
from app.database.models.telegram import User
from telebot.types import Message
from app.telegram.logger import logger


class TelegramDecorator:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.active_listeners = {}

    @staticmethod
    def __get_message(args: tuple) -> Message | None:
        for arg in args:
            if isinstance(arg, Message):
                return arg

        return None

    def __respond_not_authorised(self, message: Message):
        self.bot.reply_to(message, "⚠️ You are not authorised to preform this action.")

    def restricted(self, func):
        def wrapper(*args, **kwargs):
            if not args:
                raise RuntimeError("No args passed so a check was impossible")

            message = self.__get_message(args)
            if not message:
                raise RuntimeError("Unable to get chat_id")

            user = User.build_from_message(message)

            with UserDAO() as user_dao:
                user_exists = user_dao.exists(user.chat_id)

                if user_exists:
                    # Call the actual function
                    func(*args, **kwargs)
                else:
                    logger.warning(f"{user} Requested to use {func.__name__} but was not authorised")
                    self.__respond_not_authorised(message)

        return wrapper

    def listener(self, listener_name: str):
        """
        Decorator to register a listener for follow-up messages after a command.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                message = self.__get_message(args)
                if not message:
                    logger.error(f"Function {func.__name__}: No message instance found in args")
                    return

                chat_id = message.chat.id

                # Verify if the chat is listening for this function
                if self.active_listeners.get(chat_id) == listener_name:
                    logger.debug(f"Listener {listener_name}: Triggered for chat {chat_id}")
                    self.active_listeners.pop(chat_id, None)  # Remove listener after processing
                    return func(*args, **kwargs)

                logger.debug(f"Listener {listener_name}: Ignored for chat {chat_id} (not primed)")

            # Attach the function to Telebot's message handlers
            self.bot.message_handler(content_types=['text', 'contact', 'photo', 'document', 'voice', 'audio'], func = lambda msg: msg.chat.id in self.active_listeners)(wrapper)

            return wrapper

        return decorator

    def prime_listener(self, chat_id: int, listener_name: str) -> None:
        """Assigns a listener to a chat so that the next message is processed by that function."""
        logger.debug(f"Priming listener '{listener_name}' for chat {chat_id}")
        self.active_listeners[chat_id] = listener_name