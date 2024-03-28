from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Request, Form
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from starlette.config import Config
from starlette.responses import RedirectResponse
import httpx

config = Config(".env")
CLIENT_ID = config("CLIENT_ID", cast=str)
CLIENT_SECRET = config("CLIENT_SECRET", cast=str)
REDIRECT_URI = "http://localhost:8000/auth/callback"
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "openid email profile"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}",
    tokenUrl=TOKEN_URL,
)

test_app = FastAPI()

@test_app.get("/auth/login")
def login():
    return RedirectResponse(url=oauth2_scheme.authorizationUrl)

@test_app.get("/auth/callback")
async def callback(code: str = Depends(oauth2_scheme)):
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(TOKEN_URL, data=data)
        r.raise_for_status()
        tokens = r.json()
    return tokens
