import os

from langchain import hub
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI

from pydantic import SecretStr

from app.libs.lch.document import format_docs
from app.libs.lch.promp import log_promp
from app.libs.qdrant.vector_store import qdrant_vector_store
from app.models.question import Question


class ChatUseCase:
    def __init__(self, history: list[Question] | None = None) -> None:
        self.history = history or []

    def init_llm(self, model="gpt-4o-mini"):
        self.llm = ChatOpenAI(
            model=model,
            temperature=0,
            api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
        )

    def init_embeddings(self, model="text-embedding-3-small"):
        self.embeddings = OpenAIEmbeddings(
            model=model, api_key=os.environ["OPENAI_API_KEY"]
        )

    @property
    def history_content(self) -> str:
        return "\n".join(
            [f"question: {a.content}, answer: {a.answer}" for a in self.history[:5]]
        )

    async def ask(self, query: str):
        self.init_llm()
        prompt = PromptTemplate.from_template("""
            You are an assistant for question-answering tasks.
            If you don't know the answer, just say that you don't know and need more information.
            Use a maximum of thirty sentences and keep a concise answer.
            Here is the conversation history:
            {history}
            Question: {question} 
            Answer:
        """)

        rag_chain = (
            {"history": RunnablePassthrough(), "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | log_promp
            | StrOutputParser()
        )

        response: str = rag_chain.invoke(
            {"question": query, "history": self.history_content},
        )
        return response

    async def ask_rag(self, query: str):
        self.init_llm()
        self.init_embeddings()
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
