from app.database import MySQLConnector
from app.database.models.telegram import User


class UserDAO(MySQLConnector):
    def __init__(self):
        super().__init__()

    def __get_from_result(self, row: dict) -> User:
        invited_by_user = self.get(row["invited_by"]) if row["invited_by"] else None
        return User(chat_id = row["chat_id"], user_name = row["user_name"], full_name = row["full_name"], invited_by = invited_by_user)

    def get(self, chat_id: str) -> User | None:
        """Fetches a user by chat_id."""
        query = "SELECT chat_id, user_name, full_name, invited_by FROM user WHERE chat_id = %s"
        result = self.execute_query(query, (chat_id,))
        if result:
            return self.__get_from_result(result[0])

        return None

    def get_all(self) -> list[User]:
        """Gets all users."""
        user_list: list[User] = []
        result = self.execute_query("SELECT chat_id FROM user")
        for row in result:
            user_list.append(self.get(row["chat_id"]))

        return user_list

    def put(self, user: User) -> None:
        """Inserts or updates a user in the database."""
        query = """
        INSERT INTO user (chat_id, user_name, full_name, invited_by) 
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE user_name = VALUES(user_name), full_name = VALUES(full_name)
        """
        self.execute_update(query, (user.chat_id, user.user_name, user.full_name, user.invited_by.chat_id if user.invited_by else None))

    def exists(self, chat_id: int) -> bool:
        """Checks if a user exists in the database."""
        query = "SELECT EXISTS(SELECT 1 FROM user WHERE chat_id = %s) AS exists_flag"
        result = self.execute_query(query, (chat_id,))
        return result[0]["exists_flag"] == 1 if result else False
