import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from utils.log import Log
from conf.vars import JWT_SECRET, CLIENT_ID


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware to handle OAuth2 authentication."""
    def __init__(self, app):
        super().__init__(app)
    
    async def __call__(self, scope, receive, send) -> None:
        if scope['type'] == 'http':
            request = Request(scope, receive, send)
            try:
                await super().__call__(scope, receive, send)
            except RuntimeError as e:
                if not await request.is_disconnected():
                    Log.error(message=f'API call has failed! Error Message: {e}')
                    raise e
                Log.error(message=f'Client disconnected the API request! Error Message: {e}')
                print("remote disconnected")
        else:
            await super().__call__(scope, receive, send)

    async def dispatch(self, request: Request, call_next):
        authorization = request.headers.get('authorization')
        request.state.is_authenticated = False
        if authorization:
            token = authorization.split(" ")[-1]
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                client_id = payload.get('sub')
                if not client_id or client_id != CLIENT_ID:
                    raise HTTPException(status_code=401, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})
                request.state.is_authenticated = True
            except InvalidTokenError as error:
                Log.warning(data={'error': f'{error}'},
                            message=f'Invalid Token | Path: {request.url.path} ')

        response = await call_next(request)
        return response
