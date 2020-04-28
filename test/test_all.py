from random_word import RandomWords
import random
generate_random_word = RandomWords()


def test_home(client):
    response = client.get('/')
    assert b'Hello, Welcome to this API, Enjoy' in response.data


def test_register(client):
    no_1 = random.randint(1, 30)
    no_2 = random.randint(1, 30)
    user = f'ThisIsTestUser{no_1}{no_2}'
    password = f'QTemporalPass85#3'
    response = client.post('/auth/register', json={'username': user, 'password': password},
                           content_type='application/json', charset='UTF-8')
    assert response.status_code is 201


def test_login(client):
    user = 'UserToTestt'
    password = 'Data65##$'
    response = client.post('/auth/login', json={'username': user, 'password': password},
                           content_type='application/json', charset='UTF-8')
    assert response.status_code is 200

