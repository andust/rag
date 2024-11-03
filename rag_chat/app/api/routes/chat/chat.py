from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.api.guard.main import get_current_user
from app.models.chat import Chat
from app.models.question import Question
from app.repository.chat import chat_repository
from app.schema.chat import Ask
from app.schema.user import User
from app.usecase.chat import ChatUseCase

router = APIRouter(default_response_class=JSONResponse)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[Chat],
)
async def all_chats(user: User = Depends(get_current_user)):
    return await chat_repository.get_all()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Chat,
)
async def new_chat(user: User = Depends(get_current_user)):
    return await chat_repository.new(user_id=user.id)


@router.get(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=Chat,
)
async def get_chat(chat_id: str, user: User = Depends(get_current_user)):
    chat = await chat_repository.get(chat_id)
    if chat and user.id != chat.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not found for user")
    return chat


@router.post(
    "/ask/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[Question],
)
async def ask(chat_id: str, ask: Ask):
    questions = []
    db_chat = await chat_repository.get(chat_id)
    if db_chat:
        chat_use_case = ChatUseCase()

        answer = await chat_use_case.ask(query=ask.content)
        qst = Question(content=ask.content, answer=answer)

        questions = db_chat.questions or []
        questions.append(qst)
        db_chat.questions = questions
        await chat_repository.update(chat_id, db_chat)

    return questions
