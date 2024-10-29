from pydantic import BaseModel


class NewChat(BaseModel):
    title: str


class Ask(BaseModel):
    content: str
