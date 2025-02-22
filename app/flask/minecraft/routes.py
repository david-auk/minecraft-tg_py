from flask import jsonify
from app.database.dao.minecraft.server_dao import ServerDAO, Server
from app.tmux import TmuxSession
from . import minecraft_bp, build_new_server
from ..utils import get_params, with_server_from_request, with_session_from_db


@minecraft_bp.route('/start', methods = ["POST"])
@with_session_from_db
def start(session: TmuxSession):
    if session.is_running():
        return jsonify({'error': 'session already running'}), 500

    session.start()
    return jsonify({'message': 'session started'}), 200


@minecraft_bp.route('/stop', methods = ["POST"])
@with_session_from_db
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
            # 'id': server.id,
            'version': server.version,
            'is_running': is_running,
            'users': server.get_current_users() if is_running else []
        })

    return jsonify({'status': server_info}), 200


@minecraft_bp.route('/build-server', methods = ["POST"])
@with_server_from_request
@get_params(jar_download_url = str)
def build_server(jar_download_url: str, server: Server):

    try:
        # Download and initialize the new server
        build_new_server.build_new(jar_download_url, server)

        with ServerDAO() as server_dao:
            server_dao.put(server)

        return jsonify({'message': 'successfully_added server'}), 200
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
