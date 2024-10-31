from pydantic import BaseModel


class Ask(BaseModel):
    content: str
    document_ids: list[str]
