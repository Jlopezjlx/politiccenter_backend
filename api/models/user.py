from passlib.context import CryptContext
import re

CryptContext = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


class User:
    def __init__(self):
        self.password_hash = None

    def hash_password(self, password):
        self.password_hash = CryptContext.hash(password)
        return self.password_hash

    @staticmethod
    def verify_password(password, password_hash):
        return CryptContext.verify(password, password_hash)

    @staticmethod
    def validate_username_and_pass(username, password):
        if not username:
            return {'data': {
                'msg': 'Error registering new user, missing credentials',
                'username': 'is blank'
            }}
        if not password:
            return {'data': {
                'msg': 'Error registering new user, missing credentials',
                'password': 'is blank'
            }}
        if re.search(r"\s", username) or re.search(r"\s", password):
            return {'data': {
                'msg': 'Error registering new user, username or password has blank spaces',
            }}

