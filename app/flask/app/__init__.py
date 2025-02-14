from flask import Flask
from .minecraft import minecraft_bp


app = Flask(__name__)

app.register_blueprint(minecraft_bp, url_prefix="/minecraft")