from random_word import RandomWords
generate_random_word = RandomWords()


def test_home(client):
    rv = client.get('/')
    assert b'Hello, Welcome to this API, Enjoy' in rv.data


def test_register(client):
    user = f'{generate_random_word.get_random_word()}78'
    password = f'Q{generate_random_word.get_random_word()}85#3'
    response = client.post('/auth/register', json={'username': user, 'password': password},
                           content_type='application/json', charset='UTF-8')
    print(response.get_json())
    assert response.status_code is 201

