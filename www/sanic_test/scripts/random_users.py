import requests
import json
from app.models import User


API_URL = 'https://randomuser.me/api/'


def get_random_users(number):
    """Example response:
    {'name': {'first': 'ernesto', 'last': 'rubio', 'title': 'mr'}, 'registered': '2015-01-16 02:00:22', 'cell': '670-444-485', 'picture': {'medium': 'https://randomuser.me/api/portraits/med/men/78.jpg', 'large': 'https://randomuser.me/api/portraits/men/78.jpg', 'thumbnail': 'https://randomuser.me/api/portraits/thumb/men/78.jpg'}, 'gender': 'male', 'dob': '1994-10-16 22:55:31', 'phone': '955-747-520', 'id': {'name': 'DNI', 'value': '97307071-F'}, 'email': 'ernesto.rubio@example.com', 'login': {'sha256': '55d0bb68a63b751cffea6c6f027c5652663df2e8e0e578e4392cfc7327393c35', 'sha1': '3a79db26a30a6ddccbaab902f45fd70e1a596255', 'username': 'greenpeacock535', 'password': 'blazer', 'salt': 'RQ72U0Gj', 'md5': '93f431bd736f954d3329b30d25a39976'}, 'nat': 'ES', 'location': {'state': 'extremadura', 'city': 'las palmas de gran canaria', 'postcode': 64725, 'street': '4820 calle de arganzuela'}}
    """
    print('Calling URL', API_URL)
    
    resp = requests.get(API_URL, params=dict(results=number))

    print('Response: %s', resp.text)

    for row in resp.json().get('results', []):
        yield User(
            name = row['name']['first'],
            username = row['login']['username'],
            email = row['email'],
            password = row['login']['sha1'],
        )




# For multiple concurrent calls

# def get_random_users(number):
#     responses = []

#     @asyncio.coroutine
#     def _make_request():
#         response = yield from aiohttp.request('get', API_URL)
#         obj = (yield from response.json())
#         responses.append(obj)

#     loop = asyncio.get_event_loop()
#     tasks = [asyncio.async(_make_request()) for _ in range(number)]
#     loop.run_until_complete(asyncio.wait(tasks))

#     return responses