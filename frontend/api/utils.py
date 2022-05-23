from jose import jwt


token = None

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def decode_token(token):
    encoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return encoded_data


def get_game_id():
    global token
    encoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return encoded_data['game_id']


def is_current_user_admin():
    global token
    encoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return encoded_data['is_admin']