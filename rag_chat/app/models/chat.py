from pydantic import BaseModel

from app.models.question import Question


class Chat(BaseModel):
    id: str | None = None
    user_id: str
    questions: list[Question] | None = None

    @staticmethod
    def from_dict(data: dict):
        return Chat(
            id=str(data.get("_id")) or None,
            user_id=data.get("user_id") or "",
            questions=data.get("questions") or [],
        )
