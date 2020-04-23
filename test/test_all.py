from flask import json


def test_home(client):
    rv = client.get('/')
    assert b'Hello, Welcome to this API, Enjoy' in rv.data


def test_register(client):
    response = client.post('/auth/register', json={'username': 'User5659', 'password': 'User673##'},
                           content_type='application/json', charset='UTF-8')
    assert response.status_code is 201
    print(response.get_json())


