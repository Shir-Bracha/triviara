import json
import threading

import requests
import websocket

from api import base_url, websocket_url
from api.utils import decode_token
from api import utils


def api_move_to_next_stage():
    data = decode_token(token=utils.token)
    game_id = data["game_id"]
    requests.get(base_url+"move_to_next_stage/"+game_id)


def api_get_game_leaderboard():
    data = decode_token(token=utils.token)
    game_id = data["game_id"]
    res = requests.get(base_url+"get_game_leaderboard/"+game_id)
    return json.loads(res.content.decode('utf-8'))


def api_get_current_stage_questions():
    data = decode_token(token=utils.token)
    game_id = data["game_id"]
    res = requests.get(base_url+"get_current_stage_questions/"+game_id)
    return json.loads(res.content.decode('utf-8'))


def api_get_questions_amount():
    data = decode_token(token=utils.token)
    game_id = data["game_id"]
    res = requests.get(base_url+"get_questions_amount/"+game_id)
    return json.loads(res.content.decode('utf-8'))


def websocket_get_game_participants(game_id, on_message_func):
    wsapp = websocket.WebSocketApp(
        websocket_url+f"get_game_participants/{game_id}/ws",
        on_message=on_message_func,
    )

    wst = threading.Thread(target=wsapp.run_forever)
    wst.daemon = True
    wst.start()

    return wsapp


def websocket_get_game_current_stage(game_id, on_message_func):
    wsapp = websocket.WebSocketApp(
        websocket_url+f"get_game_current_stage/{game_id}/ws",
        on_message=on_message_func,
    )

    wst = threading.Thread(target=wsapp.run_forever)
    wst.daemon = True
    wst.start()

    return wsapp


def websocket_all_participants_answered(game_id, on_message_func):
    wsapp = websocket.WebSocketApp(
        websocket_url+f"all_participants_answered/{game_id}/ws",
        on_message=on_message_func,
    )

    wst = threading.Thread(target=wsapp.run_forever)
    wst.daemon = True
    wst.start()

    return wsapp

