from datetime import timedelta, datetime
import jwt

from conf.vars import JWT_SECRET, CLIENT_ID


def generate_access_token():
    """Generate a JWT access token."""
    to_encode = {
        "sub": CLIENT_ID,
        "exp": (datetime.now() + timedelta(minutes=30)).timestamp()
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt
