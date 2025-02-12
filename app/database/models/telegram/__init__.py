from telebot.types import Message

class User:
    def __init__(self, chat_id: int, full_name: str = None, user_name: str = None, invited_by: "User" = None):
        self.chat_id = chat_id
        self.full_name = full_name
        self.user_name = user_name
        self.invited_by = invited_by

    def __repr__(self):
        return f"<User username={self.user_name}, full_name={self.full_name}, chat_id={self.chat_id}>"

    @classmethod
    def build_from_message(cls, message: Message):
        return cls(
            chat_id=message.chat.id,
            full_name=message.from_user.full_name,
            user_name=message.from_user.username,
            invited_by = None
        )

    @classmethod
    def build_from_contact(cls, contact, invited_by: "User" = None):

        # If the user does not have a telegram account
        if not contact.user_id:
            raise RuntimeError("Contact user_id is required")

        full_name = contact.first_name
        if contact.last_name:
            full_name += f" {contact.last_name}"

        return cls(
            chat_id = contact.user_id,
            full_name = full_name,
            user_name = None,  # Contacts don’t provide a username
            invited_by = invited_by
        )