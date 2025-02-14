from functools import wraps
from flask import request, jsonify


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
