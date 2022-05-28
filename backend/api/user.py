from logic.auth import get_data_from_jwt
from logic.auth import update_access_token
from logic.game import get_game_by_id
from logic.game import get_game_user_by_username
from logic.user import answer_specific_question
from logic.user import create_new_admin_user_by_username
from logic.user import create_new_user_by_username
from logic.user import join_specific_game
from logic.user import set_specific_user_promoted_stage_flag
from main import app


@app.get("/create_new_admin_user")
async def create_new_admin_user(username: str) -> str:
    """
    :param username:
    :return:
    """
    token = create_new_admin_user_by_username(username=username)
    return token


@app.get("/create_new_user")
async def create_new_user(username: str) -> str:
    """
    :param username:
    :return:
    """
    token = create_new_user_by_username(username=username)
    return token


@app.post("/set_user_promoted_stage_flag")
async def set_user_promoted_stage_flag(game_id: str, username: str, promoted: bool) -> None:
    """
    :param game_id:
    :param username:
    :param promoted:
    :return:
    """
    game = get_game_by_id(game_id=game_id)
    set_specific_user_promoted_stage_flag(
        current_game=game,
        username=username,
        promoted=promoted
    )


@app.get("/join_game/{game_id}")
async def join_game(game_id: str, token: str) -> str:
    """
    :param game_id: the unique game identifier
    :param token:
    :return:
    """
    token_data = get_data_from_jwt(token=token)

    existing_game_id = token_data.game_id
    if existing_game_id is not None:
        raise Exception(f"User {token_data.username} is on another game, cannot join two games together.")

    join_specific_game(
        username=token_data.username,
        game_id=game_id,
    )

    updated_token = update_access_token(
        token=token,
        token_data_update={
            "game_id": game_id
        }
    )

    return updated_token


@app.post("/answer_question")
async def answer_question(question: str, answer: int, token: str) -> str:
    """
    This method receives an answer for a question and updates the participants score if the answer is correct.
    :param question: the question identifier
    :param answer: the answer identifier
    :param token:
    :return:
    """
    token_data = get_data_from_jwt(token=token)

    answer_specific_question(
        game_id=token_data.game_id,
        username=token_data.username,
        question=question,
        answer=answer
    )

    return token

