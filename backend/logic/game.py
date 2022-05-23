from typing import List
from typing import Optional
from logic.interfaces import Question
from logic.interfaces import User
from logic.interfaces import KhaootGame
from logic.data import LEADER_BOARDS
from logic.data import ALL_GAMES


def get_game_by_id(game_id: str) -> KhaootGame:
    """
    :param game_id:
    :return:
    """
    return ALL_GAMES.get(game_id)


def get_game_user_by_username(game_id: str, username: str) -> Optional[User]:
    """
    :param game_id:
    :param username:
    :return:
    """
    current_game = get_game_by_id(game_id)

    game_user = [
        user
        for user
        in current_game.participants
        if user.username == username
    ]

    if len(game_user) == 0:
        raise ValueError(f"User {username} not found.")

    return game_user[0]


def get_game_question(game: KhaootGame, question: str) -> Optional[Question]:
    """
    :param game:
    :param question:
    :return:
    """
    game_question = [
        game_question
        for game_question
        in game.questions
        if game_question.question == question
    ]

    if len(game_question) == 0:
        raise ValueError(f"Question {question} not found.")

    return game_question[0]


def did_participants_answered_all_questions(game: KhaootGame) -> bool:
    return all([user.answered for user in game.participants])


def promote_game_to_next_stage(game_id: str) -> Optional[KhaootGame]:
    """
    :param game_id:
    :return:
    """
    current_game = get_game_by_id(game_id=game_id)

    game_stages_amount = len(current_game.questions)
    next_stage = current_game.current_stage + 1


    if next_stage > game_stages_amount:
        finish_game(game_id=game_id)
        return

    # Promoting the game to the next stage
    current_game.current_stage = next_stage


    # Clearing all of the participants answered flag
    for participant in current_game.participants:
        participant.answered = False

    return current_game


def finish_game(game_id: str) -> None:
    """
    :param game_id:
    :return:
    """
    finished_game = ALL_GAMES.get(game_id, None)
    finished_game.game_ended = True

    LEADER_BOARDS[game_id] = finished_game.participants


def get_game_leaderboard_by_game_id(game_id: str) -> Optional[List[User]]:
    """
    :param game_id:
    :return:
    """
    game_leaderboard = LEADER_BOARDS.get(game_id)

    if game_leaderboard is None:
        raise ValueError(f"Failed to get game leaderboard, couldn't find game_id {game_id}.")

    return game_leaderboard


def get_specific_game_current_stage_questions(game_id: str) -> Optional[Question]:
    """
    :param game_id:
    :return:
    """
    current_game = get_game_by_id(game_id=game_id)
    if current_game is None:
        raise ValueError(f"A game with the game id: {game_id} wasn't found.")

    question_index = current_game.current_stage() -1

    game_stages_amount = len(current_game.questions)
    if question_index > game_stages_amount - 1:
        raise Exception(
            f"Failed to get stage questions, "
            f"Question stage index {question_index} is bigger then stages amount"
        )

    return current_game.questions[question_index]


def get_game_questions_amount(game_id: str) -> int:
    current_game = get_game_by_id(game_id=game_id)
    if current_game is None:
        raise ValueError(f"A game with the game id: {game_id} wasn't found.")

    return len(current_game.questions)


def get_specific_game_participants(game_id: str) -> List[User]:
    """
    :param game_id:
    :return:
    """
    current_game = get_game_by_id(game_id=game_id)
    return current_game.participants
