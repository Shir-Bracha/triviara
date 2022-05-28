from typing import List
from typing import Optional

from logic.interfaces import Question
from logic.admin import create_new_game_with_questions
from logic.admin import start_specific_game
from logic.auth import get_data_from_jwt
from logic.auth import update_access_token
from main import app


@app.post("/create_new_game")
async def create_new_game(questions: List[Question], token: str) -> str:
    """
    :param questions: a list of dictionaries of questions mapped to answers (4 answers each)
    :param token:
    :return: This method returns a link to the newly created server.
    """
    token_data = get_data_from_jwt(token=token)
    print("token_data - " + token_data.username)
    print(questions)

    new_game = create_new_game_with_questions(
        questions=questions,
        username=token_data.username
    )

    updated_token = update_access_token(
        token=token,
        token_data_update={
            "game_id": new_game.game_id
        }
    )

    return updated_token


@app.get("/start_game/{game_id}")
async def start_game(game_id: str, token: str) -> Optional[str]:
    """
    This method starts a new game with the relevant participants and sends a push notification to the user interface
    to start the game.
    :param game_id: the unique game identifier
    :return:
    """
    token_data = get_data_from_jwt(token=token)

    if not token_data.is_admin:
        raise Exception(f"User {token_data.username} is not admin, cannot start game.")

    start_specific_game(game_id=game_id)

    return token
