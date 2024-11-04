from fastapi import UploadFile, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.api.guard.main import get_current_user
from app.models.file import ChatFile
from app.repository.file import file_repository
from app.models.user import User


router = APIRouter(default_response_class=JSONResponse)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ChatFile],
)
async def all_files(user: User = Depends(get_current_user)):
    results = await file_repository.get_many()
    return results


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def new_file(files: list[UploadFile], user: User = Depends(get_current_user)):
    return await file_repository.upload_files(files=files, user_email=user.email)


@router.get(
    "/download/{file_id}",
    status_code=status.HTTP_200_OK,
)
async def download(file_id: str):
    file_data = await file_repository.get(file_id)
    return Response(content=file_data.content, media_type=file_data.content_type)
