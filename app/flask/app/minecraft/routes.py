from flask import jsonify
from app.database.dao.minecraft.server_dao import ServerDAO
from app.tmux import TmuxSession
from . import minecraft_bp, with_session
from ..utils import get_params, get_optional_params
import build_new_server


@minecraft_bp.route('/start', methods = ["POST"])
@with_session
def start(session: TmuxSession):
    if session.is_running():
        return jsonify({'error': 'session already running'}), 500

    session.start()
    return jsonify({'message': 'session started'}), 200


@minecraft_bp.route('/stop', methods = ["POST"])
@with_session
def stop(session: TmuxSession):
    if not session.is_running():
        return jsonify({'error', 'session not running'}), 500

    session.stop()
    return jsonify({'message': 'session stopped'}), 200


@minecraft_bp.route('/status', methods = ["GET"])
def status():
    with ServerDAO() as server_dao:
        servers = server_dao.get_all()

    server_info = []
    for server in servers:
        session = TmuxSession(server)
        is_running = session.is_running()
        server_info.append({
            'name': server.name,
            'version': server.version,
            'is_running': is_running,
            'users': server.get_current_users() if is_running else []
        })

    return jsonify({'status': server_info}), 200


@minecraft_bp.route('/new-server', methods = ["POST"])
@get_params(server_name=str, server_version=str, jar_download_url=str, java_min_ram=int, java_max_ram=int)
@get_optional_params(properties=dict)
def new_server(server_name: str, server_version: str, jar_download_url: str, java_min_ram: int, java_max_ram: int,
               properties: dict = None):

    try:
        server = build_new_server.build(
            server_name = server_name,
            server_version = server_version,
            jar_download_url = jar_download_url,
            min_ram = java_min_ram,
            max_ram = java_max_ram,
            properties = properties or {}
        )

        with ServerDAO() as server_dao:
            server_dao.put(server)

        return jsonify({'message': 'successfully_added server'}), 200
    except Exception as e:
        return jsonify({'error': str(e)})
