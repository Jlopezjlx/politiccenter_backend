from flask import Flask, abort, request, jsonify
import re


class User:
    def validate_username_and_pass(self, username, password):
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

