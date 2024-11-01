from contextlib import contextmanager
import os

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant
from pydantic import SecretStr

from app.config.envirenment import get_settings
from app.libs.lch.document import recursive_character_text_splitter

_S = get_settings()


@contextmanager
def upload_documents(docs: list[Document]):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", api_key=SecretStr(os.environ["OPENAI_API_KEY"])
    )
    qdrant = Qdrant.from_documents(
        recursive_character_text_splitter(docs),
        embeddings,
        url=_S.QDRANT_URL,
        collection_name=_S.QDRANT_MAIN_DOCUMANTS,
    )
    try:
        yield qdrant
    finally:
        qdrant.client.close()
        embeddings.client
