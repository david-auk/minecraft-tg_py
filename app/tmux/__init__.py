from app.database.models.minecraft import Server
import subprocess


def get_all_running_sessions():
    result = subprocess.run(['tmux', 'list-sessions', '-F', '\"#S\"'], stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE, text = True)
    if result.returncode == 1:
        return []
    else:
        return [session.strip('"') for session in result.stdout.strip().split('\n')]


class TmuxSession:
    def __init__(self, server: Server):
        self.server = server
        self.session_name = f"{server.server_path}_session"

    def is_running(self) -> bool:
        return self.session_name in get_all_running_sessions()

    def start(self):
        if self.is_running():
            raise RuntimeError("Session already running")

        # (Over)Write the current config file
        self.server.update_properties()

        subprocess.run(['tmux', 'new-session', '-d', '-s', self.session_name, '-c', self.server.server_path,
                        self.server.get_start_cmd()])

    def stop(self):
        if not self.is_running():
            raise RuntimeError("Session is not running")

        subprocess.run(['tmux', 'send-keys', '-t', self.session_name, 'C-c'])
