from src.auth.models import User
from src.auth.schemas import JWTDataScheme


class AuthService:

    @classmethod
    async def authenticate_user(cls, jwt_data: JWTDataScheme) -> User:
        pass
