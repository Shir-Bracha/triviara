import requests
from api import base_url
from api import utils
from api.utils import decode_token


def api_create_new_admin_user(username):
    res = requests.get(base_url+"create_new_admin_user", params={"username":username})
    utils.token = res.content.decode('utf-8')[1:-1]


def api_create_new_user(username):
    res = requests.get(base_url+"create_new_user", params={"username":username})
    utils.token = res.content.decode('utf-8')[1:-1]


def api_join_game(game_id):
    res = requests.get(base_url+"join_game/" +game_id, params={"token": utils.token})
    utils.token = res.content.decode('utf-8')[1:-1]


def api_answer_question(question, answer):
    requests.post(
        base_url+"answer_question",
        params={"question": question, "answer": answer, "token": utils.token}
    )


def api_set_user_promoted_stage_flag(promoted_stage):
    data = decode_token(token=utils.token)
    game_id = data["game_id"]
    username = data["username"]

    requests.post(
        base_url+"set_user_promoted_stage_flag",
        params={"game_id": game_id, "username": username, "promoted": promoted_stage}
    )
