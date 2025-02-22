from app.database.models.minecraft import Server
import os
import requests
import subprocess

server_root = os.environ.get("MINECRAFT_SERVER_ROOT")


def __accept_eula(server: Server):
    # Construct the full path to the eula.txt file
    eula_path = os.path.join(server_root, server.server_path, "eula.txt")

    # Read the existing content from the EULA file
    with open(eula_path, 'r') as file:
        lines = file.readlines()

    # Update the line that sets the EULA agreement to true
    new_lines = []
    for line in lines:
        # If this line starts with "eula=" then replace its value with true
        if line.strip().lower().startswith("eula="):
            new_lines.append("eula=true\n")
        else:
            new_lines.append(line)

    # Write the updated content back to the EULA file
    with open(eula_path, 'w') as file:
        file.writelines(new_lines)


def get_filename_without_extension(filename):
    while True:
        filename, ext = os.path.splitext(filename)
        if not ext:
            break
    return filename


def __download_jar_file(jar_download_url: str) -> str:
    response = requests.get(jar_download_url, stream = True)
    if response.status_code != 200:
        raise Exception(f"Failed to download JAR file: {response.status_code}")

    jar_file_name = jar_download_url.split("/")[-1]
    jar_file_path = os.path.join(server_root, jar_file_name)
    with open(jar_file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size = 8192):
            file.write(chunk)

    return jar_file_name


def __run_server(server: Server):
    # Construct the working directory path by joining the root path with the server's specific path
    workdir = os.path.join(server_root, server.server_path)

    # Output the start command and working directory for debugging purposes
    print(f"Starting server with command: {server.get_start_cmd()} in directory: {workdir}", flush = True)

    # Run the start command in the specified working directory, capturing the output and error messages
    process = subprocess.run(
        server.get_start_cmd(),  # The list of arguments for the command to execute
        cwd = workdir,  # Set the current working directory for the command
        capture_output = True,  # Capture both stdout and stderr from the command
        text = True  # Return output as text (string), not bytes
    )

    # Output the results of the command execution (stdout, stderr) for debugging purposes
    print(f"Command executed with return code: {process.returncode}", flush = True)
    print(f"Standard Output: {process.stdout}", flush = True)
    if process.stderr:
        print(f"Standard Error: {process.stderr}", flush = True)


def build_new(jar_download_url: str, server: Server) -> None:
    # Get vars
    jar_file_name = __download_jar_file(jar_download_url)
    jar_file_path = os.path.join(server_root, jar_file_name)
    server.java_settings.server_file = jar_file_name

    # Get the new server dir
    server_path = os.path.join(server_root, server.server_path)

    if os.path.exists(server_path):
        raise RuntimeError("Server already initialised")

    # Create the new server path
    os.makedirs(server_path, exist_ok = True)

    # Move the JAR to the designated dir
    os.rename(jar_file_path, os.path.join(server_path, jar_file_name))

    # Run the server for EULA generation (with other files)
    __run_server(server)

    # Accept the EULA
    __accept_eula(server)

    # Write the custom properties to the newly generated property file
    server.update_properties()
