from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class ChatFile(BaseModel):
    id: str | None
    filename: str
    length: int
    upload_date: datetime | None

    @staticmethod
    def from_dict(data: dict):
        return ChatFile(
            id=str(data.get("_id")) or None,
            filename=data.get("filename") or "-",
            length=data.get("length") or 0,
            upload_date=data.get("uploadDate"),
        )


class FileData(BaseModel):
    content: bytes
    content_type: Literal["application/pdf", "text/plain", "text/csv"]

    def to_text(self) -> str:
        if self.content_type == "text/plain":
            return str(self.content)

        raise ValueError("can't convert to text")
