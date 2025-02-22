from flask import Flask
from app.flask.minecraft import minecraft_bp
from os import getenv

app = Flask(__name__)

app.register_blueprint(minecraft_bp, url_prefix="/minecraft")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = getenv("FLASK_RUN_PORT"))
