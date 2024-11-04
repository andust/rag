from contextlib import contextmanager
from langchain_qdrant import QdrantVectorStore
from app.config.envirenment import get_settings

_S = get_settings()


@contextmanager
def qdrant_vector_store(embeddings):
    try:
        qdrant = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            url=_S.QDRANT_URL,
            collection_name=_S.QDRANT_MAIN_DOCUMANTS,
        )
        yield qdrant
    finally:
        qdrant.client.close()
