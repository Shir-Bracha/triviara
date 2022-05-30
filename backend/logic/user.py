import json
from typing import Optional

from logic.data import ALL_GAMES_MAP
from logic.data import CURRENT_USERS_MAP
from logic.data import REDIS_CONNECTION
from logic.interfaces import KhaootGame
from logic.interfaces import User
from logic.auth import TokenData
from logic.auth import create_access_token
from logic.game import get_game_by_id
from logic.game import get_game_question
from logic.game import get_game_user_by_username


# This is the amount of score to be added to a user if answered the correct answer.
SCORE_UNIT = 10


def create_new_admin_user_by_username(username: str) -> Optional[str]:
    is_user_exists = REDIS_CONNECTION.hget(CURRENT_USERS_MAP, username)

    if is_user_exists:
        raise ValueError(f"Username {username} is already taken.")

    new_user = User(username=username)
    REDIS_CONNECTION.hset(CURRENT_USERS_MAP, username, new_user.json())

    token_data = TokenData(
        is_admin=True,
        username=username
    )

    token = create_access_token(
        data=token_data
    )

    return token


def create_new_user_by_username(username: str) -> Optional[str]:
    is_user_exists = REDIS_CONNECTION.hget(CURRENT_USERS_MAP, username)

    if is_user_exists:
        raise ValueError(f"Username {username} is already taken.")

    new_user = User(username=username)
    REDIS_CONNECTION.hset(CURRENT_USERS_MAP, username, new_user.json())

    token_data = TokenData(
        is_admin=False,
        username=username
    )

    token = create_access_token(
        data=token_data
    )

    return token


def get_current_user_by_username(username: str) -> User:
    """
    :return: the current user model by the JWT.
    """
    current_user = User(**json.loads(REDIS_CONNECTION.hget(CURRENT_USERS_MAP, username)))
    return current_user


def join_specific_game(username: str, game_id: str) -> Optional[KhaootGame]:
    """
    :return:
    """
    current_user = get_current_user_by_username(username=username)
    current_game = get_game_by_id(game_id=game_id)

    participants_amount = len(current_game.participants)
    if participants_amount >= 6:
        raise Exception(f"Too many players in game {game_id}.")

    current_game.participants.append(current_user)

    REDIS_CONNECTION.hset(ALL_GAMES_MAP, game_id, current_game.json())

    return current_game


def check_if_user_answered(game_id: str, username: str) -> bool:
    """
    :param username:
    :return:
    """
    user = get_game_user_by_username(
        game_id=game_id,
        username=username
    )

    if user.answered:
        return True

    return False


def check_if_answer_correct(game: KhaootGame, question: str, answer: int) -> bool:
    """
    :param game:
    :param question:
    :param answer:
    :return:
    """
    current_question = get_game_question(game=game, question=question)

    return current_question.correct_answer == answer


def update_user_score(user: User) -> None:
    user.score += SCORE_UNIT


def check_answer(game_id: str, username: str, question: str, answer: int) -> None:
    """
    :param game_id:
    :param username:
    :param question:
    :param answer:
    :return:
    """
    current_game = get_game_by_id(game_id=game_id)
    is_answer_correct = check_if_answer_correct(
        game=current_game,
        question=question,
        answer=answer,
    )

    for game_user in current_game.participants:
        if game_user.username == username:
            if is_answer_correct:
                update_user_score(user=game_user)

            game_user.answered = True

            REDIS_CONNECTION.hset(ALL_GAMES_MAP, game_id, current_game.json())
            break


def answer_specific_question(game_id: str, username: str, question: str, answer: int) -> None:
    """
    :param game_id:
    :param username:
    :param question:
    :param answer:
    :return:
    """
    is_answered = check_if_user_answered(
        game_id=game_id,
        username=username,
    )

    if is_answered:
        raise ValueError(f"User {username} already answered this question.")

    check_answer(
        game_id=game_id,
        username=username,
        question=question,
        answer=answer,
    )


def set_specific_user_promoted_stage_flag(current_game: KhaootGame, username: str, promoted: bool) -> None:
    for user in current_game.participants:
        if user.username == username:
            user.promoted_stage = promoted

            REDIS_CONNECTION.hset(ALL_GAMES_MAP, current_game.game_id, current_game.json())
            break


def set_all_users_need_to_be_promoted_flag(current_game: KhaootGame, promoted: bool) -> None:
    for participant in current_game.participants:
        set_specific_user_promoted_stage_flag(
            current_game=current_game,
            username=participant.username,
            promoted=promoted
        )


def check_if_user_needs_to_be_promoted_stage(game: KhaootGame) -> bool:
    return any([user.promoted_stage for user in game.participants])
