from flask import Flask, g
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import os
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, get_raw_jwt
)

from . import routes


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    with app.app_context():
        routes.init_app(app)
        mysql = MySQL(app)
        jwt = JWTManager(app)

    @app.route('/')
    def home():
        return 'Hello, Welcome to this API, Enjoy'

    return app
