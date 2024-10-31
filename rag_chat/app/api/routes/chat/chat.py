import os

from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import SecretStr

from app.api.guard.main import get_current_user
from app.lch.main import generate_response
from app.models.chat import Chat
from app.models.question import Question
from app.repository.chat import chat_repository
from app.repository.file import file_repository
from app.schema.chat import Ask
from app.schema.user import User

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


@router.post(
    "/ask/{chat_id}",
    status_code=status.HTTP_200_OK,
    response_model=Chat,
)
async def ask(chat_id: str, ask: Ask):
    db_chat = await chat_repository.get(chat_id)
    if db_chat:
        file_documents = await file_repository.get_many(ask.document_ids)

        qst = Question(content=ask.content)
        documents = [a.to_text() for a in file_documents]

        answer = generate_response(
            documents=documents,
            openai_api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
            query_text=qst.content,
        )
        qst.answer = answer

        questions = db_chat.questions or []
        questions.append(qst)
        db_chat.questions = questions
        await chat_repository.update(chat_id, db_chat)

    return db_chat
