from pydantic import BaseModel


class Ask(BaseModel):
    content: str
