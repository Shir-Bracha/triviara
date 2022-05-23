from typing import Dict
from typing import List

from logic.interfaces import KhaootGame
from logic.interfaces import User


# This dictionary holds all of the currently running Khaoot games, and maps them by their unique game_id.
ALL_GAMES: Dict[str, KhaootGame] = {}

# Users details along with their scores mapped to game id.
LEADER_BOARDS: Dict[str, List[User]] = {}

# Current users dictionary, username to User class mapping.
CURRENT_USERS: Dict[str, User] = {}