from typing import List
from pydantic import BaseModel


class User(BaseModel):
    username: str
    score: int = 0
    answered: bool = False


class Question(BaseModel):
    question: str
    correct_answer: int
    answers: List[str]


class KhaootGame(BaseModel):
    """
    This class represents a single khaoot game structure.
    """
    game_id: str
    participants: List[User]
    current_stage: int = 0
    questions: List[Question]
    game_ended: bool = False
