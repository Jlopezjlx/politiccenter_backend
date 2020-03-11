from flask import Flask, abort, request, jsonify
import re


class User:
    def validate_username_and_pass(self, username, password):
        if not username or not password:
            return jsonify({'data': {
                'msg': 'Error registering new user, missing credentials',
                'username': username
            }}), 400

        if re.search(r"\s", username) or re.search(r"\s", password):
            return jsonify({'data': {
                'msg': 'Error registering new user, username or password has blank spaces',
                'username': username
            }}), 400

