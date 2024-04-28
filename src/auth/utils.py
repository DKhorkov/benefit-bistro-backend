from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.auth.config import URLPathsConfig, jwt_config
from src.auth.schemas import JWTDataScheme


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=URLPathsConfig.TOKEN)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def get_password_hash(password):
    return pwd_context.hash(secret=password)


def create_access_token(jwt_data: JWTDataScheme):
    jwt_token = jwt.encode(
        claims=jwt_data.model_dump(),
        key=jwt_config.ACCESS_TOKEN_SECRET_KEY,
        algorithm=jwt_config.ACCESS_TOKEN_ALGORITHM
    )
    return jwt_token
