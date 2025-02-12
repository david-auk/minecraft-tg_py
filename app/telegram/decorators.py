from app.database.dao.telegram.user_dao import UserDAO
from telebot.types import Message


class TelegramDecorator:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def __get_message(args: tuple) -> Message:
        for arg in args:
            if isinstance(arg, Message):
                return arg

        return None

    def __respond_not_authorised(self, message: Message):
        self.bot.reply_to(message, "Not authorised")

    def authorised_arg(self, func):
        def wrapper(*args, **kwargs):
            if not args:
                raise RuntimeError("No args passed so a check was impossible")

            message = self.__get_message(args)
            if not message:
                raise RuntimeError("Unable to get chat_id")

            chat_id = message.chat.id

            with UserDAO() as user_dao:

                for u in user_dao.get_all():
                    print(u.name, u.chat_id)

                user_exists = user_dao.exists(chat_id)  # TODO Fix

                print(chat_id, user_exists, flush = True)

                if user_exists:
                    # Call the actual function
                    func(*args, **kwargs)
                else:
                    self.__respond_not_authorised(message)

        return wrapper
