import requests
from api import base_url
from api import utils
from api.utils import decode_token


def api_create_new_game(questions):
    res = requests.post(base_url+"create_new_game", params={"token": utils.token}, json=questions)
    utils.token = res.content.decode('utf-8')[1:-1]


def api_start_game():
    data = decode_token(token=utils.token)
    game_id = data["game_id"]
    res = requests.get(base_url + "start_game/" + game_id, params={"token": utils.token})
    utils.token = res.content.decode('utf-8')[1:-1]

