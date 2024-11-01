import os
from contextlib import contextmanager

from langchain import hub
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI

from pydantic import SecretStr
from langchain_qdrant import QdrantVectorStore

from app.config.envirenment import get_settings
from app.libs.lch.document import format_docs

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


def log_promp(a):
    print("-" * 25)
    print(a)
    print("-" * 25)
    return a


class ChatUseCase:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
        )
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", api_key=os.environ["OPENAI_API_KEY"]
        )

    async def ask(self, query: str):
        with qdrant_vector_store(self.embeddings) as vector_store:
            retriever = VectorStoreRetriever(
                vectorstore=vector_store,
                search_type="similarity",
                search_kwargs={"k": 3},
            )
            prompt = hub.pull("rlm/rag-prompt")

            rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | log_promp
                | StrOutputParser()
            )

            response: str = rag_chain.invoke(query)
            return response

        return ""
