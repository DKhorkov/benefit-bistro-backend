from fastapi import Request
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from jose import jwt
from passlib.context import CryptContext
from typing import Optional, Dict

from src.auth.config import URLPathsConfig, jwt_config, cookies_config, passlib_config
from src.auth.models import JWTDataModel
from src.auth.exceptions import NotAuthenticated


class OAuth2Cookie(OAuth2):
    """
    Class uses OAuth2 to retrieve token for user authentication from cookies.
    """

    def __init__(
        self,
        token_url: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Retrieves token for user authentication from cookies, if exists.
        """

        token: Optional[str] = request.cookies.get(cookies_config.COOKIES_KEY)
        if not token:
            if self.auto_error:
                raise NotAuthenticated
            else:
                return None
        return token


pwd_context: CryptContext = CryptContext(
    schemes=[passlib_config.PASSLIB_SCHEME],
    deprecated=passlib_config.PASSLIB_DEPRECATED
)

oauth2_scheme: OAuth2Cookie = OAuth2Cookie(token_url=URLPathsConfig.LOGIN)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


async def hash_password(password: str) -> str:
    return pwd_context.hash(secret=password)


async def create_access_token(jwt_data: JWTDataModel) -> str:
    jwt_token: str = jwt.encode(
        claims=await jwt_data.to_dict(),
        key=jwt_config.ACCESS_TOKEN_SECRET_KEY,
        algorithm=jwt_config.ACCESS_TOKEN_ALGORITHM
    )
    return jwt_token
