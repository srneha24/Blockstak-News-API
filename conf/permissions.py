from fastapi import HTTPException, Request

from utils.log import Log


class IsAuthenticated:
    """Permission Class For Authencation of Users"""

    async def __call__(self, request: Request):
        if not request.state.is_authenticated:
            Log.warning(message=f'Authentication Failed | path: {request.url.path}')
            raise HTTPException(detail='Authentication Failed! Invalid Credentials!', status_code=401)
        return None
