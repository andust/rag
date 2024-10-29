from pydantic import BaseModel


class Question(BaseModel):
    content: str
    answer: str = ""
