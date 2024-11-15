import requests

from passlib.context import CryptContext
from cachetools import cached, TTLCache

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # 'tokenUrl' is a placeholder


keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    verify=True
)

# Create a cache with a TTL of 10 minutes
public_key_cache = TTLCache(maxsize=1, ttl=settings.CACHE_TTL_DURATION)

@cached(cache=public_key_cache)
def get_public_key():
    return keycloak_openid.public_key()

def decode_token(token: str):
    try:
        public_key = get_public_key()
        options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
        token_info = keycloak_openid.decode_token(token, key=public_key, options=options)
        return token_info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")