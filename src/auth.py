import os
from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from beartype import beartype
from dotenv import load_dotenv
from jwt import ExpiredSignatureError, InvalidTokenError

from src.logger import log_execution

load_dotenv()


class JWTAuth:
    def __init__(self):
        self.SECRET_KEY = os.getenv("JWT_SECRET")

    @log_execution
    @beartype
    async def generate_jwt(self, user_id: int) -> str:
        """Gera um token JWT para um usuário"""
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
        return token

    @log_execution
    @beartype
    async def verify_jwt(self, auth_header: str) -> Union[str, bool]:
        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return True
        except ExpiredSignatureError:
            return "Token expirado"
        except InvalidTokenError:
            return "Token inválido"
