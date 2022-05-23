from typing import Dict
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class TokenData(BaseModel):
    is_admin: bool
    username: str
    game_id: Optional[str] = None


def create_access_token(data: TokenData) -> str:
    to_encode = data.dict().copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def update_access_token(token: str, token_data_update: Dict) -> str:
    jwt_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    jwt_data.update(token_data_update)

    encoded_jwt = jwt.encode(jwt_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_data_from_jwt(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        jwt_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if jwt_data is None:
            raise credentials_exception

        token_data = TokenData(
            is_admin=jwt_data.get('is_admin'),
            game_id=jwt_data.get('game_id'),
            username=jwt_data.get('username'),
        )
    except JWTError:
        raise credentials_exception

    return token_data
