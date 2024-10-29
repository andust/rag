import uuid

from fastapi import status, Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from app.api.guard.main import get_current_user
from app.models.chat import Chat
from app.models.question import Question
from app.schema.chat import Ask, NewChat
from app.schema.user import User


router = APIRouter(default_response_class=JSONResponse)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Chat,
)
async def new_chat(new_chat: NewChat, user: User = Depends(get_current_user)):
    db_chat = await Chat.find_one({"user_id": user.id, "title": None})
    if not db_chat:
        db_chat = Chat(user_id=user.id, title=None)
        await db_chat.save()

    return db_chat


@router.post(
    "/ask/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=Chat,
)
async def ask(chat_id: str, ask: Ask):
    chat = await Chat.get(chat_id)
    if chat:
        qst = Question(content=ask.content)

        qst.answer = f"{uuid.uuid4().hex}"
        if chat.questions is None:
            chat.questions = []
        chat.questions.append(qst)
        await chat.save()

    return chat
