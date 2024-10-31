from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.chat import Chat
from app.db.main import db


class ChatRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def new(self, user_id: str) -> Chat | None:
        db_chat = await self.collection.find_one({"user_id": user_id, "question": None})
        if not db_chat:
            new_chat = Chat(user_id=user_id)
            result = await self.collection.insert_one(new_chat.model_dump())
            new_chat.id = str(result.inserted_id)

            return new_chat

        return Chat.from_dict(db_chat)

    async def get(self, id: str) -> Chat | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        if document:
            return Chat.from_dict(document)
        return None

    async def get_all(self) -> list[Chat]:
        return await self.collection.find({}).to_list()

    async def update(self, id: str, data: Chat) -> Chat | None:
        document = data.model_dump(exclude_unset=True, by_alias=True)
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": document}
        )
        if result.modified_count:
            return await self.get(id)
        return None


chat_repository = ChatRepository(collection=db["chats"])
