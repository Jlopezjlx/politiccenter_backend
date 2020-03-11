from flask import Flask, abort, request, jsonify
from passlib.apps import custom_app_context as pwd_context
from flask_mysqldb import MySQL
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, get_raw_jwt
)
from dotenv import load_dotenv
import os
import re
import sys
sys.path.append("./")
from queries.db_queries import PoliticCenterQueries

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

mysql = MySQL(app)
jwt = JWTManager(app)
PoliticCenterQueries = PoliticCenterQueries()
blacklist = set()


class User:
    def __init__(self):
        self.password_hash = None

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        return self.password_hash

    def verify_password(self, password, password_hash):
        return pwd_context.verify(password, password_hash)


def validate_password(password):
    validator = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
    if re.match(validator, password):
        return True
    else:
        return False


@jwt.expired_token_loader
def is_token_expired(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401


@jwt.invalid_token_loader
def is_token_expired(expired_token):
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The token is invalid'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/api/users/logout', methods=['DELETE', 'POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@app.route('/api/test')
@jwt_required
def test():
    return 'hola test'


@app.route('/api/users/refresh_token', methods=['GET', 'POST'])
@jwt_refresh_token_required
def get_token():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@app.route('/api/users/login', methods=['POST'])
def login():
    _user = User()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'data': {
            'msg': 'Error, missing credentials'
        }}), 401
    try:
        user_info = PoliticCenterQueries.get_user_info(username=username, mysql=mysql)
        checked = _user.verify_password(password, user_info.get('pass_hash'))
        if checked:
            ret = {
                'access_token': create_access_token(identity=username),
                'refresh_token': create_refresh_token(identity=username)
            }
            return jsonify(ret), 200
        else:
            return jsonify({'data': {
                'msg': 'Error, incorrect password'
            }}), 401
    except:
        return jsonify({'data': {
            'msg': 'Error, incorrect credentials'
        }}), 401


@app.route('/api/users/register', methods=['POST'])
def new_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    current_username = PoliticCenterQueries.get_user_info(username=username, mysql=mysql)
    if username is None or password is None:
        abort(400)  # missing arguments
    if current_username and current_username.get('username') == username:
        return jsonify({'data': {
            'msg': 'Error registering new user, this user already exist',
            'username': username
        }}), 400
    pass_checker = validate_password(password=password)
    if pass_checker:
        user = User()
        try:
            pass_hash = user.hash_password(password)
            cur = mysql.connection.cursor()
            cur.execute("insert into users(username, pass_hash) values(%s, %s)", (username, pass_hash))
            mysql.connection.commit()
            cur.close()
            return jsonify({'data': {
                'msg': 'Successful',
                'username': username
            }}), 201
        except:
            return jsonify({'data': {
                'msg': 'Error registering new user',
                'username': username
            }}), 400
    else:
        return jsonify({'data': {
            'msg': 'Error registering new user, password does not fill requirements',
            'username': username
        }}), 400


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
