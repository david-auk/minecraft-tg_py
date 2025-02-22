from flask import Blueprint
minecraft_bp = Blueprint('minecraft', __name__)

from . import routes
