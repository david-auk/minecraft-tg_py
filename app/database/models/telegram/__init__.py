from telebot.types import Message

class User:
    def __init__(self, chat_id: int, full_name: str , user_name: str, invited_by):
        self.chat_id = chat_id
        self.full_name = full_name
        self.user_name = user_name
        self.invited_by: User = invited_by

    def __repr__(self):
        return f"<User username={self.user_name}, full_name={self.full_name}, chat_id={self.chat_id}>"

    @staticmethod
    def build_from_message(message: Message):
        return User(
            chat_id=message.chat.id,
            full_name=message.from_user.full_name,
            user_name=message.from_user.username,
            invited_by = None
        )