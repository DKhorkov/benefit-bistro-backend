from src.auth.models import UserModel
from src.auth.schemas import JWTDataScheme


class AuthService:

    @classmethod
    async def authenticate_user(cls, jwt_data: JWTDataScheme) -> UserModel:
        pass
