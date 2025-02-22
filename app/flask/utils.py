from functools import wraps
from flask import request, jsonify
from app.database.models.minecraft import Server, JavaSettings
from app.database.dao.minecraft.server_dao import ServerDAO
from app.tmux import TmuxSession


def get_params(**expected_params):
    """
    Decorator to extract and validate JSON POST parameters.

    :param expected_params: Dictionary of expected parameter names and their types.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Missing JSON body'}), 400

            extracted_params = {}

            for param, param_type in expected_params.items():
                value = data.get(param)

                if value is None:
                    return jsonify({'error': f'Missing {param}'}), 400

                if not isinstance(value, param_type):
                    return jsonify({'error': f'{param} must be of type {param_type.__name__}'}), 400

                extracted_params[param] = value

            return f(*args, **extracted_params, **kwargs)

        return decorated_function

    return decorator


def get_optional_params(**expected_params):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}  # Ensure data is at least an empty dict
            extracted_params = {}

            for param, param_type in expected_params.items():
                if param in data:  # Only validate if the key exists
                    value = data[param]
                    if not isinstance(value, param_type):
                        return jsonify({'error': f'{param} must be of type {param_type.__name__}'}), 400
                    extracted_params[param] = value

            return f(*args, **extracted_params, **kwargs)

        return decorated_function
    return decorator


def with_java_settings(f):
    @get_params(server_file=str, min_ram=int, max_ram=int)
    @wraps(f)
    def decorated_function(server_file: str, min_ram: int, max_ram: int, *args, **kwargs):
        java_settings = JavaSettings(server_file=server_file, min_ram=min_ram, max_ram=max_ram)
        return f(java_settings=java_settings, *args, **kwargs)

    return decorated_function  # Ensure the decorated function is returned


def with_server_from_request(f):

    @with_java_settings
    @get_params(server_name=str, server_path=str, server_version=str, properties=dict)
    @wraps(f)
    def decorated_function(server_name: str, server_path: str, server_version: str, properties: dict,
                           java_settings: JavaSettings, *args, **kwargs):
        server = Server(
            name=server_name,
            server_path=server_path,
            version=server_version,
            properties=properties,
            java_settings=java_settings
        )
        return f(server=server, *args, **kwargs)

    return decorated_function  # Ensure the decorated function is returned


def with_server_from_db(f):
    @get_params(server_id=str)  # Reuse get_params to validate and extract server_id
    @wraps(f)
    def decorated_function(server_id, *args, **kwargs):
        with ServerDAO() as server_dao:
            server = server_dao.get(server_id)

        if not server:
            return jsonify({'error': 'server_id not found'}), 500

        return f(server=server, *args, **kwargs)

    return decorated_function  # Ensure the decorated function is returned


def with_session_from_db(f):
    @with_server_from_db
    @wraps(f)
    def decorated_function(server: Server, *args, **kwargs):
        return f(session=TmuxSession(server), *args, **kwargs)  # Pass the session as a parameter

    return decorated_function  # Ensure the decorated function is returned
