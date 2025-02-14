from functools import wraps
from flask import Flask, flash, request, jsonify
from app.database.dao.minecraft.server_dao import ServerDAO
from app.tmux import TmuxSession
from . import minecraft_bp


def with_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        server_id = data.get('server_id')

        if not server_id:
            return jsonify({'error': 'Missing server_id'}), 500

        with ServerDAO() as server_dao:
            server = server_dao.get(server_id)

        if not server:
            return jsonify({'error': 'server_id not found'}), 500

        session = TmuxSession(server)
        return f(session, *args, **kwargs)  # Pass the session as a parameter

    return decorated_function


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
    with ServerDAO as server_dao:
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

    return jsonify({'status', server_info}), 200
