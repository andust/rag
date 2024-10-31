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
        documents = [
            "This is the Fundamentals of RAG course. Educative is an AI-powered online learning platform. There are 4 Generative AI courses available on Educative. I am writing this using my keyboard. JavaScript is a good programming language",
        ]

        qst = Question(content=ask.content)
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
