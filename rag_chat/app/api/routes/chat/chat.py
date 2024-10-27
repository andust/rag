from fastapi import status, Request
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


router = APIRouter(default_response_class=JSONResponse)


class Question(BaseModel):
    user_id: str
    content: str


@router.post(
    "/ask",
    status_code=status.HTTP_200_OK,
    response_model=Question,
)
async def ask(request: Request, question: Question):
    return question
