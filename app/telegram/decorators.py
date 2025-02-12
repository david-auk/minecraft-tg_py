from app.database.dao.telegram.user_dao import UserDAO
from app.database.models.telegram import User
from telebot.types import Message
from app.telegram.logger import logger


class TelegramDecorator:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def __get_message(args: tuple) -> Message | None:
        for arg in args:
            if isinstance(arg, Message):
                return arg

        return None

    def __respond_not_authorised(self, message: Message):
        self.bot.reply_to(message, "Not authorised to preform this action.")

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
