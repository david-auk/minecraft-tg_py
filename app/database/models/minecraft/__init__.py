from mcrcon import MCRcon

default_properties = {
    "rcon.port": "25575",
    "rcon.password": "default_password"
}


class JavaSettings:
    def __init__(self, server_file: str, min_ram: int, max_ram: int):
        self.server_file = server_file
        self.min_ram = min_ram
        self.max_ram = max_ram


class Server:
    def __init__(self, name: str, version: str, server_path: str, java_settings: JavaSettings, properties=None):
        if properties is None:
            properties = default_properties
        self.name = name
        self.version = version
        self.server_path = server_path
        self.java_settings = java_settings
        self.properties = properties if properties else default_properties

        required_properties = ["rcon.port", "rcon.password"]
        for required_property in required_properties:
            if not required_property in self.properties.keys():
                raise RuntimeError(f"Missing required property: {required_property}")

    def get_rcon_session(self) -> MCRcon:
        port = self.properties["rcon.port"]
        password = self.properties["rcon.password"]
        return MCRcon("localhost", password, port)

    def get_start_cmd(self):
        return (f'java -Xmx{self.java_settings.max_ram}M -Xms{self.java_settings.min_ram}M'
                f' -jar {self.java_settings.server_file} nogui')

    def __get_server_properties_filename(self) -> str:
        return f'{self.server_path}/server.properties'

    def __read_properties(self) -> dict[str, str]:
        config_file = self.__get_server_properties_filename()

        # Read the content of the configuration file
        with open(config_file, 'r') as file:
            lines = file.readlines()

        properties = {}
        for line in lines:
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
        for property_key, property_val in properties:
            lines.append(f"{property_key}={property_val}")

        # Write the modified content back to the file
        with open(config_file, 'w') as file:
            file.writelines(lines)

    def update_properties(self):
        self.__write_properties_to_file(self.__get_properties())

    def get_current_users(self) -> list[str]:
        pass  # TODO implement

    def __repr__(self):
        return f"<Server name={self.name}, version={self.version}, path={self.server_path}>"
