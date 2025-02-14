from flask import Blueprint

minecraft_bp = Blueprint('auth', __name__)

from . import routes
