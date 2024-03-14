from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from config import AUTH_PASS


cookie_transport = CookieTransport(cookie_max_age=3600)

AUTH_PASS = AUTH_PASS

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=AUTH_PASS, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
