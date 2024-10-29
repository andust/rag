from beanie import Document

from app.models.question import Question


class Chat(Document):
    user_id: str
    title: str | None = None
    questions: list[Question] | None = None

    class Settings:
        name = "chats"
