from typing import List
import uuid
from logic.interfaces import KhaootGame
from logic.interfaces import Question
from logic.data import ALL_GAMES
from logic.game import get_game_by_id
from logic.user import get_current_user_by_username


def create_new_game_with_questions(questions: List[Question], username: str) -> KhaootGame:
    """
    :param questions: a list of dictionaries of questions mapped to answers (4 answers each)
    :return: This method returns a link to the newly created server.
    """
    new_game_id = uuid.uuid4().hex[:7]
    current_user = get_current_user_by_username(username=username)
    new_game = KhaootGame(
        game_id=new_game_id,
        participants=[current_user],
        current_stage=0,
        questions=questions,
    )

    ALL_GAMES[new_game_id] = new_game

    return new_game


def start_specific_game(game_id: str) -> None:
    """
    :param game_id:
    :return:
    """
    current_game = get_game_by_id(game_id=game_id)

    if current_game.current_stage != 0:
        raise Exception("Game already started")

    current_game.current_stage = 1
