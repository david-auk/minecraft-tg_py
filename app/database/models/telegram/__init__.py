class User:
    def __init__(self, chat_id: str, name: str, invited_by):
        self.chat_id = chat_id
        self.name = name
        self.invited_by: User = invited_by
