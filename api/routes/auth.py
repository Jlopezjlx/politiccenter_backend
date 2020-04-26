import re
import sys

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, get_raw_jwt
)
from flask_mysqldb import MySQL

sys.path.append("./")
from api.db.db_queries import PoliticCenterQueries
from api.models.user import User

mysql = MySQL()
jwt = JWTManager()
PoliticCenterQueries = PoliticCenterQueries()
blacklist = set()
User_validation = User()

bp = Blueprint("login", __name__, url_prefix="/auth")


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


@bp.route('/logout', methods=['DELETE', 'POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@bp.route('/test')
@jwt_required
def verify():
    return 'hola test'


@bp.route('/refresh_token', methods=['GET', 'POST'])
@jwt_refresh_token_required
def get_token():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@bp.route('/login', methods=['POST'])
def login():
    _user = User()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'data': {
            'msg': 'Error, missing credentials'
        }}), 401
    if re.search(r"\s", username) or re.search(r"\s", password):
        return jsonify({'data': {
            'msg': 'Error, username or password has blank spaces',
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


@bp.route('/register', methods=['POST'])
def new_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    current_username = PoliticCenterQueries.get_user_info(username=username, mysql=mysql)
    user_validation_response = User_validation.validate_username_and_pass(username, password)
    if user_validation_response:
        return jsonify(user_validation_response), 400
    if current_username:
        if current_username.get('username') == username:
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
