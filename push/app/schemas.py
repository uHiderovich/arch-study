from pydantic import BaseModel


class PushPayload(BaseModel):
    subscription: dict
    title: str
    body: str
