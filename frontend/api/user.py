import requests
from api import base_url
from api import utils


def api_create_new_admin_user(username):
    res = requests.get(base_url+"create_new_admin_user",params={"username":username})
    utils.token = res.content.decode('utf-8')[1:-1]


def api_create_new_user(username):
    res = requests.get(base_url+"create_new_user",params={"username":username})
    utils.token = res.content.decode('utf-8')[1:-1]


def api_join_game(game_id):
    res = requests.get(base_url+"join_game/" +game_id,params={"token": utils.token})
    utils.token = res.content.decode('utf-8')[1:-1]


def api_answer_question(question,answer):
    res = requests.get(base_url+"answer_question/" +question+"/"+str(answer),params={"token": utils.token})
    utils.token = res.content.decode('utf-8')[1:-1]
