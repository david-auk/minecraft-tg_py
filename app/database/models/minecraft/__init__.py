from mcrcon import MCRcon
import os

required_properties = {
    "rcon.port": "25575",
    "rcon.password": "default_password"
}

forced_properties = {
    "enable-rcon": "true"
}


server_root = os.environ.get("MINECRAFT_SERVER_ROOT")


class JavaSettings:
    def __init__(self, server_file: str, min_ram: int, max_ram: int):
        self.server_file = server_file
        self.min_ram = min_ram
        self.max_ram = max_ram


class Server:
    def __init__(self, name: str, version: str, server_path: str, java_settings: JavaSettings, properties=None):
        self.name = name
        self.version = version
        self.server_path = server_path
        self.java_settings = java_settings
        self.properties = properties if properties else required_properties

        for required_property_key, default_value in required_properties.items():
            if not required_property_key in self.properties.keys():
                properties[required_property_key] = default_value

        for key, value in forced_properties.items():
            properties[key] = value  # Overwrite the forced properties

    def get_rcon_session(self) -> MCRcon:
        port = self.properties["rcon.port"]
        password = self.properties["rcon.password"]
        return MCRcon("localhost", password, port)

    def get_start_cmd(self) -> list:
        return [
            'java',
            f'-Xmx{self.java_settings.max_ram}M',
            f'-Xms{self.java_settings.min_ram}M',
            '-jar',
            self.java_settings.server_file,
            'nogui'
        ]

    def __get_server_properties_filename(self) -> str:
        return os.path.join(server_root, f'{self.server_path}/server.properties')

    def __read_properties(self) -> dict[str, str]:
        config_file = self.__get_server_properties_filename()

        # Read the content of the configuration file
        with open(config_file, 'r') as file:
            lines = file.readlines()

        properties = {}
        for line in lines:

            # Skip comments
            if line.startswith("#"):
                continue

            key, value = line.split("=")
            properties[key] = value

        return properties

    def __get_properties(self):

        properties = self.__read_properties()

        for property_key, property_val in self.properties.items():
            # (over)Write custom properties
            properties[property_key] = property_val

        return properties

    def __write_properties_to_file(self, properties: dict[str, str]):

        config_file = self.__get_server_properties_filename()

        lines = []
        for property_key, property_val in properties.items():

            property_val_txt = str(property_val)
            if type(property_val) is bool:
                property_val_txt = property_val_txt.lower()

            lines.append(f"{property_key}={property_val_txt}\n")

        # Write the modified content back to the file
        with open(config_file, 'w') as file:
            file.writelines(lines)

    def update_properties(self):
        self.__write_properties_to_file(self.__get_properties())

    def run_command(self, command: str) -> str:

        # Check if the command starts with a / and add it if not
        if not command.startswith('/'):
            command = f"/{command}"

        with self.get_rcon_session() as mcrcon:
            output = mcrcon.command(command)

        return output

    def get_current_users(self) -> list[str]:
        pass  # TODO implement

    def __repr__(self):
        return f"<Server name={self.name}, version={self.version}, path={self.server_path}>"
