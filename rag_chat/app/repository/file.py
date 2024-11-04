from bson import ObjectId
from fastapi import UploadFile
from langchain_core.documents import Document
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from app.constants.file import POSSIBLE_CONTENT_TYPE
from app.db.main import db
from app.libs.qdrant.upload_document import upload_documents
from app.models.file import FileData, ChatFile


class FileRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        # TODO use protocol to abstract collection
        self.collection = collection

    async def get_file_content_type(self, id: str) -> str | None:
        result = await self.collection.find_one(
            {"_id": ObjectId(id)}, projection={"metadata.content_type": 1, "_id": 0}
        )

        if result:
            return result["metadata"]["content_type"]

        return

    async def get(self, id: str) -> FileData:
        """_summary_

        Parameters
        ----------
        id : str
            file id

        Returns
        -------
        FileData
            file content data
        """
        # TODO use protocol to abstract this class
        fs = AsyncIOMotorGridFSBucket(db)

        file_content = await self.get_file_content_type(id)
        grid_out = await fs.open_download_stream(ObjectId(id))
        content = await grid_out.read()

        return FileData(content=content, content_type=file_content)

    async def get_many_by_ids(self, ids: list[str]) -> list[FileData]:
        result = []
        # TODO use protocol to abstract this class
        # limit param
        fs = AsyncIOMotorGridFSBucket(db)
        files = (
            await fs.find({"_id": {"$in": [ObjectId(a) for a in ids]}})
            .sort("uploadDate", -1)
            .limit(20)
            .to_list()
        )
        for file in files:
            result.append(await self.get(file["_id"]))

        return result

    async def get_many(self) -> list[ChatFile]:
        # TODO use protocol to abstract this class
        # limit param
        fs = AsyncIOMotorGridFSBucket(db)
        most_recent_three = await fs.find().sort("uploadDate", -1).limit(3).to_list()

        return [ChatFile.from_dict(a) for a in most_recent_three]

    async def upload_files(self, files: list[UploadFile], user_email: str) -> list[str]:
        # TODO use protocol to abstract this class
        fs = AsyncIOMotorGridFSBucket(db)

        file_ids = []
        docs: list[Document] = []
        for file in files:
            if file.content_type in POSSIBLE_CONTENT_TYPE:
                content = file.file.read()
                file_id = await fs.upload_from_stream(
                    file.filename or "no-name",
                    content,
                    metadata={"content_type": file.content_type, "user": user_email},
                )
                file_ids.append(str(file_id))
                docs.append(
                    Document(
                        page_content=str(content),
                        metadata={"file_id": str(file_id), "title": file.filename},
                    )
                )

        with upload_documents(docs=docs):
            ...

        return file_ids


file_repository = FileRepository(collection=db["fs.files"])
