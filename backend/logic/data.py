import redis


REDIS_CONNECTION = redis.StrictRedis(
    host='<enter_host>',
    port=<enter_port>,
    password='<enter_your_passowrd>',
    ssl=False,
)

# This dictionary holds all of the currently running Khaoot games, and maps them by their unique game_id.
ALL_GAMES_MAP = "ALL_GAMES"

# Users details along with their scores mapped to game id.
LEADER_BOARDS_MAP = "LEADER_BOARDS"

# Current users dictionary, username to User class mapping.
CURRENT_USERS_MAP = "CURRENT_USERS"
