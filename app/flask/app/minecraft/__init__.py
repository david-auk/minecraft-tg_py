from functools import wraps
from flask import Blueprint, jsonify
from ..utils import get_params
from app.database.dao.minecraft.server_dao import ServerDAO
from app.tmux import TmuxSession

minecraft_bp = Blueprint('auth', __name__)

from . import routes


def with_session(f):
    @get_params(server_id=str)  # Reuse get_params to validate and extract server_id
    @wraps(f)
    def decorated_function(server_id, *args, **kwargs):
        with ServerDAO() as server_dao:
            server = server_dao.get(server_id)

        if not server:
            return jsonify({'error': 'server_id not found'}), 500

        session = TmuxSession(server)
        return f(session, *args, **kwargs)  # Pass the session as a parameter

    return decorated_function
