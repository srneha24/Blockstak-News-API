import hashlib
import random
import string
from fastapi import APIRouter, Request, HTTPException
from cachetools import TTLCache

from utils.token import generate_access_token
from conf.response import CustomJSONResponse
from conf.vars import DEFAULT_CLIENT_HASH


router = APIRouter(
    prefix="",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

cache = TTLCache(maxsize=5, ttl=300)


@router.get("/code")
async def get_code(_request: Request, client_id: str):
    """Endpoint to get a code."""
    length = random.randint(8, 10)
    code = ''.join(
        random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
        for _ in range(length)
    )
    cache[client_id] = code
    return CustomJSONResponse(content={"code": code})


@router.get("/token")
async def get_token(_request: Request, client_id: str, client_secret: str, code: str):
    """Endpoint to get a token."""
    client = f"client_id:{client_id}-client_secret:{client_secret}"
    md5_hash = hashlib.md5()
    md5_hash.update(client.encode('utf-8'))
    client_hash = md5_hash.hexdigest()
    if client_hash != DEFAULT_CLIENT_HASH:
        raise HTTPException(status_code=400, detail="Client Not Found")
    cached_code = cache.get(client_id)
    if not cached_code:
        raise HTTPException(status_code=400, detail="Code Expired")
    if code != cached_code:
        raise HTTPException(status_code=400, detail="Invalid Code")
    access_token = generate_access_token()
    return CustomJSONResponse(content={"token": access_token})
