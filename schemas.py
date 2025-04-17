from pydantic import BaseModel


class Client(BaseModel):
    client_secret: str
