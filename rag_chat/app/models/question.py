from typing import Literal
from pydantic import BaseModel


class Question(BaseModel):
    content: str
    context: Literal["rag", "chat"] = "chat"
    answer: str = ""

