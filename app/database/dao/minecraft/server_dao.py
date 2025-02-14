from app.database import MySQLConnector
from app.database.models.minecraft import Server, JavaSettings


class ServerDAO(MySQLConnector):
    def __init__(self):
        super().__init__()

    def __get_from_result(self, row: dict) -> Server:
        """Converts a database row into a Server object."""
        properties = self.get_properties(row["id"])
        java_settings = self.get_java_settings(row["id"])

        return Server(
            name = row["name"],
            version = row["version"],
            server_path = row["server_path"],
            properties = properties,
            java_settings = java_settings
        )

    def get(self, name: str) -> Server | None:
        """Fetches a server by name."""
        query = "SELECT id, name, version, server_path FROM servers WHERE name = %s"
        result = self.execute_query(query, (name,))
        if result:
            return self.__get_from_result(result[0])

        return None

    def get_all(self) -> list[Server]:
        """Gets all servers."""
        server_list: list[Server] = []
        result = self.execute_query("SELECT id, name, version, server_path FROM servers")
        for row in result:
            server_list.append(self.__get_from_result(row))

        return server_list

    def put(self, server: Server) -> None:
        """Inserts or updates a server in the database."""
        query = """
        INSERT INTO servers (name, version, server_path) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE version = VALUES(version), server_path = VALUES(server_path)
        """
        self.execute_update(query, (server.name, server.version, server.server_path))

        # Get the server ID for inserting properties
        server_id = self.get_id(server.name)

        if server_id:
            self.put_properties(server_id, server.properties)
            self.put_java_settings(server_id, server.java_settings)

    def exists(self, name: str) -> bool:
        """Checks if a server exists in the database."""
        query = "SELECT EXISTS(SELECT 1 FROM servers WHERE name = %s) AS exists_flag"
        result = self.execute_query(query, (name,))
        return result[0]["exists_flag"] == 1 if result else False

    def get_id(self, name: str) -> int | None:
        """Fetches the ID of a server by name."""
        query = "SELECT id FROM servers WHERE name = %s"
        result = self.execute_query(query, (name,))
        return result[0]["id"] if result else None

    def get_properties(self, server_id: int) -> dict:
        """Fetches server properties."""
        query = "SELECT property_name, property_value FROM server_properties WHERE server_id = %s"
        result = self.execute_query(query, (server_id,))
        return {row["property_name"]: row["property_value"] for row in result}

    def put_properties(self, server_id: int, properties: dict) -> None:
        """Inserts or updates server properties."""
        for key, value in properties.items():
            query = """
            INSERT INTO server_properties (server_id, property_name, property_value)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE property_value = VALUES(property_value)
            """
            self.execute_update(query, (server_id, key, value))

    def get_java_settings(self, server_id: int) -> JavaSettings:
        """Fetches Java settings."""
        query = "SELECT server_file, min_ram, max_ram FROM java_settings WHERE server_id = %s"
        result = self.execute_query(query, (server_id,))
        return result[0] if result else {}

    def put_java_settings(self, server_id: int, java_settings: JavaSettings) -> None:
        """Inserts or updates Java settings."""
        query = """
        INSERT INTO java_settings (server_id, server_file, min_ram, max_ram)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE server_file = VALUES(server_file), min_ram = VALUES(min_ram), max_ram = VALUES(max_ram)
        """
        self.execute_update(query, (
            server_id, java_settings.server_file, java_settings.min_ram, java_settings.max_ram))
