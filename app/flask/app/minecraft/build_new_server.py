from app.database.models.minecraft import JavaSettings, Server
import os


def get_filename_without_extension(filename):
    while True:
        filename, ext = os.path.splitext(filename)
        if not ext:
            break
    return filename


def __download_jar_file(jar_download_url: str) -> str:
    pass # TODO implement and return filename


def build(server_name: str, server_version: str, jar_download_url: str, min_ram: int, max_ram: int, properties: dict[str, str] = None) -> Server:

    jar_file_name = __download_jar_file(jar_download_url)
    settings = JavaSettings(jar_file_name, min_ram, max_ram)

    return Server(
        name = server_name,
        server_path = f"{get_filename_without_extension(jar_file_name)}_{server_version}",
        version = server_version,
        properties = properties,
        java_settings = settings
    )

    pass
    # TODO Step 1: Download file
    # TODO Step 2: Run that file
    # TODO Step 3: Check and accept eula
    # TODO Step 4: Regenerate and build world and server_properties (ideally on a different port for running servers)
    # TODO Step 5: Exit server after all is done (DIFFICULT TO AUTOMATE)
    # TODO Step 6: Return a Minecraft Server instance
