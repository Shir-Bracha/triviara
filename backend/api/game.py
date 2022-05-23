import asyncio
from typing import List
from fastapi import WebSocket

from logic.game import did_participants_answered_all_questions
from logic.game import get_game_by_id
from logic.game import get_game_questions_amount
from logic.game import get_specific_game_participants
from logic.interfaces import User
from logic.interfaces import Question
from logic.game import get_game_leaderboard_by_game_id
from logic.game import get_specific_game_current_stage_questions
from logic.game import promote_game_to_next_stage
from main import app


@app.get("/move_to_next_stage/{game_id}")
async def move_to_next_stage(game_id: str) -> None:
    """
    This method triggers if all of the users answered their questions or on timeout and act as follows for a given game:
    * promotes the stage field
    * checks if the game is over
    :param game_id: the unique game identifier
    :return:
    """
    promote_game_to_next_stage(game_id=game_id)


@app.get("/get_game_leaderboard/{game_id}")
async def get_game_leaderboard(game_id: str) -> List[User]:
    """
    :param game_id:
    :return:
    """
    return get_game_leaderboard_by_game_id(game_id=game_id)


@app.get("/get_current_stage_questions/{game_id}")
async def get_current_stage_questions(game_id: str) -> Question:
    """
    :param game_id: the unique game identifier
    :return:
    """
    return get_specific_game_current_stage_questions(game_id=game_id)


@app.get("/get_questions_amount/{game_id}")
async def get_questions_amount(game_id: str) -> Question:
    """
    :param game_id: the unique game identifier
    :return:
    """
    return get_game_questions_amount(game_id=game_id)


@app.websocket("/get_game_participants/{game_id}/ws")
async def get_game_participants(websocket: WebSocket, game_id: str) -> None:
    """
    this method returns concurrently the list of all of the game participants.
    """
    await websocket.accept()

    while True:
        users_list = get_specific_game_participants(game_id=game_id)
        serialized_users_list = [user.dict() for user in users_list]
        await websocket.send_json(serialized_users_list)
        await asyncio.sleep(1)


@app.websocket("/all_participants_answered/{game_id}/ws")
async def all_participants_answered(websocket: WebSocket, game_id: str) -> None:
    """
    this method returns concurrently the list of all of the game participants.
    """
    await websocket.accept()

    while True:
        current_game = get_game_by_id(game_id=game_id)
        did_all_participants_answered = did_participants_answered_all_questions(game=current_game)
        await websocket.send_json(did_all_participants_answered)
        await asyncio.sleep(1)


@app.websocket("/get_game_current_stage/{game_id}/ws")
async def get_game_current_stage(websocket: WebSocket, game_id: str) -> None:
    """
    this method returns concurrently the current stage for a given game.
    """
    await websocket.accept()

    while True:
        current_game = get_game_by_id(game_id=game_id)
        current_stage = current_game.current_stage
        await websocket.send_json(current_stage)
        await asyncio.sleep(1)
